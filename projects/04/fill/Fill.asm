// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen
// by writing 'black' in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen by writing
// 'white' in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(BEGIN) // begin the infinite loop
  @SCREEN
  D=A
  @R0
  M=D

(STATUS) // STATUS status
  @KBD
  D=M
  @BLACK
  D;JGT	// if keys pressed black
  @WHITE
  D;JEQ	// otherwise white
  @STATUS
  0;JMP

(BLACK)
  @R1
  M=-1 // black
  @UPDATE
  0;JMP

(WHITE)
  @R1
  M=0	// white
  @UPDATE
  0;JMP

(UPDATE)
  @R1	// black or white
  D=M
  @R0
  A=M	// address to fill in the screen
  M=D
  @R0
  D=M+1	// next pixel
  @KBD
  D=A-D
  @R0
  M=M+1	// next pixel
  A=M
  @UPDATE
  D;JGT	// if black exit
  @BEGIN
  0;JMP