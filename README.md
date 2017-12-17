# arrows-esolang

Arrows is meant to be a graphic, stack-based esoteric language with the following
qualities:

1. Every operation and value in the language is a drawn arrow.  
2. Values are encoded as distance traveled along an arrow.  
3. Stack operations are encoded as turns within an arrow.  
4. Conditionals are encoded as double ended arrows.

The stack operations are:  
1. Turn up: Push the current value onto the left stack.
2. Turn down: Push the current value onto the right stack.
3. Turn left: Pop x from the left stack, and subtract x from the current value.  
4. Turn right: Pop x from the right stack, and subtract x from the current value.  

There are two types of arrow heads:  
1. Plain arrows. Simply continue forward until you hit another arrow.  
2. Out arrows. Have two extra pixels at the back of the arrow head. Outputs the current value as an ASCII character.  

There are three types of arrow rears:  
1. Plain rear. Nothing special.  
2. Start rear. The back of an arrow that has one extra pixel signals the
starting location of a program.  
3. Input rear. The back of an arrow that has two extra pixels signals that
when entered from the direction the arrow is facing that one character
should be read in and stored as the current value.

> Arrows in your eyes  
> Fear where your heart should be  
> War in your mind  
> Shame in your cries

\- Arrows - Foo Fighters
