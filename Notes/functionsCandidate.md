Functions candidate 1
Have a system of 4 parallel lists to describe any component. (The currently imoplemented system of identifying a component's data only uses 2 lists)
These 4 lists would be:
* Component Name "parent.name" or just ".name" if no parent.
* Component argument count: the amount of arguments the component needs to function.
* Function index: Just 0 if it is not a function, but if it is a function, this points towards where the start of it is.
* Function Length: Tells how many lines to execute before returning to where the pointer was before it jumped to the function.
Core concept of Function Candidate 1:
THE FUNCTION MEGA-LIST
Filled with a ton of functions right on startup and registered onto the 4 parallel lists.
There is no actual separator between each function like there is inside of LIMB. This system just relies on the Function Length attribute from the 4 parallel lists.
Process of calling a function when using Candidate 1:
1. Identify function name.
2. Identify Arguments.
3. Accept Arguments. (Load into their temporary holder)
4. MARK position.
5. Set Instruction Pointer (IP) to the Function's Index with an "f" added to the beginning. e.g. f12, f405. This tells the scheduler not to feed the component reader content from the process's code, but from the function code.
6. Run entirety of function until RETURN is called.
7. Return to MARK.

Functions Candidate 2
Main Idea of 2nd Candidate:
Every process points to the LIMB that contain's its code.
That pointer stays the same, no matter how much the IP changes.
There can be a separate stack that controlls the process's pointers and allows the use of any citrus as the current executing code.
Instead of just having a single pointer, a process can request to have a list of pointers instead.
Here is an example pointer list:
3 - This points to a LIMB containing the original code of the process when it was registered.
7 - This could be a separate LIMB that is not a registered process, but contains valid Citrus. Therefore, it could be used as a function.
When it is done running something from the list, it deletes its index, and when there are no more indexes, the process is ended.
Supporting Concept of Candidate 2:
The instruction pointer is moved to the very begining of the process's LIMB that contains its code.
This means that each LIMB has its own unique pointer, so that you don't have to juggle the same pointer around when switching between LIMBS in your LIMB stack, and that a pointer is automatically deleted when the LIMB is.

"Functions Candidate 2" Will now be the accepted method. Expect changes to the method, refer to latest documentations of the method rather than the candidate.

To support the new Functions Candidate, a redefinition is required.
The main idea of the functions now changes the main idea of how Citrus is executed.
Instead of 