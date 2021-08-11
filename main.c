//
// VIP 2015
// (c) 2015 Dbug / Defence Force
//

#include <lib.h>


void main()
{
	paper(0);
	ink(0);
	hires();
	
	
	//
	// Install the irq handler
	//
    DigiPlayer_InstallIrq();
	

	while (1)
	{
		
    }
}




/*

Some more design stuff:
- TEXT screen goes from $BB80 to $BFDF
- HIRES screen goes from $A000 to $BFDF
- The usable STD charset is from $b400+8*32 to $b400+8*(32+96)
                                 $B400+256 to $B400+1024
                                 $B500 to $B7FF

$B500-$A000=5376 / 40 = 134.4
$B800-$A000=6144 / 40 = 153.6

154-134=20 lines

134/8 -> 16.75

For each line:
HIRES ATTRIBUTE TEXT


TechTech history:
- 
- November 1987 - Amiga    - TechTech by Sodan & Magician42 -> http://www.pouet.net/prod.php?which=4445   (http://www.sodan.dk)
- December 1989 - Atari ST -  grodan and kvack kvack (Sowatt Demo) by The Carebears   -> http://www.pouet.net/prod.php?which=754
- March 2004    - Windows  - Ported to pc -> http://www.pouet.net/prod.php?which=11934



November 1987
Sodan & Magician 42
release
Tech Tech
on the Amiga
-
December 1989
The Carebears
convert it in
Grodan and Kvack Kvack
on the Atari ST

FontleroyBrown 20

--------------------
In November 1987
Sodan & Magician 42
released Tech Tech
on the Amiga.

In December 1989
The Carebears
converted it into
Grodan and Kvack Kvack
for the Atari ST.

In May 2005
Defence Force
realized it could not be done
on the Oric but tried anyway !!!
-----------------------


*/





