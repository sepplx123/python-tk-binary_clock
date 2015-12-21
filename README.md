# python-tk-binary_clock
Binary Clock with rotation segments
Python 2.7.10 and tkinter

Original idea from: http://www.bartelmus.org/binar-uhr/#more-136


Hallo liebe Leute,

ich versuche diese Binäruhr auf der Webseite http://www.bartelmus.org/binar-uhr/#more-136 nachzubauen.

Es gibt da aber noch ein Verständnisproblem, wie genau die Animation funktioniert.

Ich habe es so verstanden, dass nach genau 24h der äußerste Zeiger genau 1 Umdrehung vollzogen hat.
Die anderen Zeiger dann entsprechend nachfolgender Tabelle:
Also Zeiger 5 1 Umdrehung, Zeiger 4 macht 16, Zeiger 3 128, Zeiger 2 512 und Zeiger 1 1024.
24h entspricht 24*60*60s = 86400s
-----------------------------------------------------------------------------
Zeiger 1 2 * 1/2 2 8 64 1024 * 360° =>> 1024*360°/86400s ==> 4,2666 °/s
Zeiger 2 4 * 1/4 1 4 32 512 * 360° =>> 512*360°/86400s ==> 2,1333 °/s
Zeiger 3 8 * 1/8 1 8 128 * 360° =>>
Zeiger 4 16 * 1/16 1 16 * 360° =>>
Zeiger 5 32 * 1/32 1 * 360° =>>

Andere Vorschläge?
