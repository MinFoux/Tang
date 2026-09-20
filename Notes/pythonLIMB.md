 # How LIMB works in Python
 
 Because I want LIMB to actually be somewhat of a challenge, and faithful to Tang's philosophy, LIMB in the python edition of Tang will be 100% made of Bytes.
 Currently, the program is using 256 8 character strings as RAM. 
 Now, how will this work? I don't know. I've been brainstorming though. Here is what i've come up with.
 
 The first item of LIMB will probably be a byte showing how long the address list is. This address list is groups of two bytes. These two bytes point towards a section of code. The first one says where it is located, and the seconds says how long it is.
 To start, I should probably test this system. 
 Steps:
 
 1. Check the 1st item of LIMB for the length of the address list.
 2. Check the 2nd item of LIMB for the first available space in the Adress list that data can be put into.
 3. Insert the index of where you want your data to exist in LIMB, and where you want it to end.
 4. Create your 3 pieces of data. Your starting point; which describes where the ending point is, your First Available Space index; which is essentially the lenght of your array, and the ending point, which describes the index of the start of the array.

As far as I know, this system is foolproof, but I know it most likely needs some work if I have ever programmed before. (Which I have) 