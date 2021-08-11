## Script to convert audio file into sample array to replay with digiplayer
## Author : Jean-Baptiste PERIN
## Date : 2021

import sys, argparse, os, math, struct, random
import soundfile
from scipy import signal
from pydub import AudioSegment

def buffer2asmCode(theName, theBuffer):
    theCode = ""
    first = True
    nline = False
    for ii in range(len(theBuffer)):
        if nline == True:
            theCode += f"\n\t.byt "
            nline = False
        elif first:
            theCode += f"_{theName}\n\t.byt "
            first = False
        else:
            theCode += ", "
        if (theBuffer[ii] < 0):
            intv = struct.unpack('B',struct.pack("b", theBuffer[ii]))[0]
        else:
            intv = theBuffer[ii]
        theCode += f"{intv}"
        if ((ii+1) %16 == 0) and (ii != 0):
            # theCode += "\n\t.byt "
            nline = True

    return theCode

def buffer2cCode(theName, theType, theBuffer):
    theCode = ""
    first = True
    for ii in range(len(theBuffer)):
        if first:
            theCode += f"{theType} {theName}[] = {{\n\t"
            first = False
        else:
            theCode += ", "
        theCode += f"{theBuffer[ii]}"
        if ((ii+1) %16 == 0) and (ii != 0):
            theCode += "\n\t"
    theCode += "};\n"
    return theCode


def encodeSample(x):
    'sample x is between -1.0 and 1.0 included'
    return 0 if (x==0) else max(0,min(15,round(15 - math.log2(1.0/(x/2 + 0.5)**2))))

def samples2buffer (data):
    buffer      = []
    new_byte    = False
    tmp_val     = None
    for sample in data:
        if new_byte:
            #buffer.append (tmp_val * 16 + encodeSample(sample) )
            buffer.append (16 *encodeSample(sample) + tmp_val )
        else:
            tmp_val = encodeSample(sample)
        new_byte = not new_byte
    return buffer

def readAudioDataFromFile(soundfilename, channels=None, samplerate=None, subtype=None):
    filename, file_extension = os.path.splitext(soundfilename)
    if (file_extension == '.raw'):
        audio_data, samplerate = soundfile.read(soundfilename, dtype='float64', channels=channels, samplerate=samplerate, subtype=subtype);
    else:
        try:
            audio_data, samplerate = soundfile.read(soundfilename, dtype='float64')
        except:
            if ((not os.path.exists('ffmpeg.exe')) or (not os.path.exists('ffprobe.exe'))):
                try:
                    sound = AudioSegment.from_file(soundfilename)
                except :
                    print ("ERROR Unrecognized file format")
                    return None, None
                temp_file_name = filename+'_'+''.join(random.choice('0123456789ABCDEF') for i in range(16))+'.wav'
                sound.export(temp_file_name, format="wav")
                audio_data, samplerate = soundfile.read(temp_file_name, dtype='float64')
                os.remove(temp_file_name)
            else:
                print ('ERROR Unrecognized File Format .. Try installing ffmpeg ')
                return None, None
    return audio_data, samplerate 

def processAudioFile(args):

    audio_data, samplerate = readAudioDataFromFile(args.soundfile, args.channels, args.samplerate, args.subtype)
    if (not audio_data or not samplerate): return 

    # Converting STEREO to MONO if required
    if (len(audio_data.shape) > 1):
        audio_data = (audio_data[:,0] + audio_data[:,1]) / 2

    # Resampling audio 
    new_number_of_samples = round(len(audio_data) * float(args.replayFrequency) / samplerate)
    out_data = signal.resample(audio_data, new_number_of_samples)    

    out_buffer = samples2buffer (out_data)
    if (args.language == 'asm'):
        out_code = buffer2asmCode(args.outputVariableName, out_buffer)
        fileext = '.s'
        out_code += f"\n_{args.outputVariableName}End"
    else:
        out_code = buffer2cCode(args.outputVariableName, "unsigned char", out_buffer)
        fileext = '.c'
    with open(args.outputFilenameRadical+fileext, 'w') as outfil:
        outfil.write(out_code)

def main(arguments):
    parser = argparse.ArgumentParser(
        prog='SampleTweaker'
        , description='Sample tweaker for Oric replaying'
        , epilog = '''For example:
        '''
        )
    parser.add_argument("soundfile"
                        , help="audio file to convert (VAV,MP3, OGG, FLAC ...)"
                        )
    parser.add_argument('--rfreq'
                        , help="replay frequency"
                        , type=int
                        , default=4000
                        , dest = 'replayFrequency'
                        )
    parser.add_argument('--outrad'
                        , default="sample"
                        , help="radical of the output file name"
                        , dest = 'outputFilenameRadical'
                        )
    parser.add_argument('--outvar'
                        , default="sample"
                        , help="name of the variable to be created"
                        , dest = 'outputVariableName'
                        )
    parser.add_argument('--language'
                        , default="asm"
                        , help=" type of generated file [c | asm] "
                        , choices=["c", "asm"]
                        )
    parser.add_argument('--nchan'
                        , help="number of channel in audio file (only for RAW audio file)"
                        , type=int
                        , choices=[1, 2]
                        , dest = 'channels'
                        )
    parser.add_argument('--samplerate'
                        , help="sampling frequency of audio file (only for RAW audio file)"
                        , type=int
                        , dest = 'samplerate'
                        )
    parser.add_argument('--subtype'
                        , help="type of encoding (only for RAW audio file)"
                        , choices=['PCM_S8','PCM_16','PCM_24','PCM_32','PCM_U8','FLOAT','DOUBLE','ULAW','ALAW','GSM610','DWVW_12','DWVW_16','DWVW_24','VOX_ADPCM']
                        , dest = 'subtype'
                        )
    args = parser.parse_args(arguments)

    if (not os.path.isfile(args.soundfile)): 
        print (f"ERROR: Unable to find input file {args.soundfile}")
        return 
    filename, file_extension = os.path.splitext(args.soundfile)
    if (file_extension == '.raw'):
        if (args.channels == None or args.samplerate == None or args.subtype == None):
            print (f"ERROR: For RAW files, you have to specify option --nchan --samplerate and --subtype")
            return
    else:
        if (args.channels != None or args.samplerate != None or args.subtype != None):
            print (f"WARNING: For non RAW files options --nchan --samplerate and --subtype are ignored (values are deduced from audio file)")

    if (args.replayFrequency > 8000):
        print (f"ERROR: replay frequency higher then 8kHz are not possible on Oric. Check --rfreq value")
        return 
        
    processAudioFile(args)

if __name__ == "__main__":
    # main (['-h'])
    # main('SampleTweaker sexample_8k_u8pcm_mono.wav'.split()[1:])
    # main('SampleTweaker sexample_44k_f64_stereo.wav'.split()[1:])
    # main('SampleTweaker sexample_192kpbs_stereo.mp3'.split()[1:])
    # main('SampleTweaker sexample_44kHz_qual5_stereo.ogg'.split()[1:])
    # main('SampleTweaker sexample_44kHz_lev5_16bits_stereo.flac'.split()[1:])
    # main('SampleTweaker sexample_4kHz_u8pcm_mono.raw --nchan 1 --samplerate 4000 --subtype PCM_U8 --outvar WelcomeSample'.split()[1:])
    # main('SampleTweaker requirements.txt'.split()[1:])
    main (sys.argv[1:])
