#Inicio do Jogo

.START __main__

.DATA
  guesses 4
  key -2

.CODE

DEF __main__:
  PUSH "Guess a number between 1 and 20 in three tries!\n"
  PUSH 2
  CALL WRITE
  PUSH 2
  PUSH 20
  RAND
  MUL
  ADD
  TRUNC
  STOR key
  LOAD key
:start
  PUSH "Try #"
  PUSH 4
  LOAD guesses
  SUB
  PUSH ". What's your guess? "
  PUSH 3
  CALL WRITE
  CALL READ
  TRUNC
  CMP key
  JZ :win
  JLESS :bigger
  JMORE :lower
:bigger
  PUSH "The number is bigger!\n"
  PUSH 2
  CALL WRITE
  JP :continue
:lower
  PUSH "The number is lower!\n"
  PUSH 2
  CALL WRITE
:continue
  POP
  LOAD guesses
  PUSH 2
  SUB
  CMP 0
  JZ :game_over
  STOR guesses
  JP :start
:win
  PUSH "Congratulations! The number was "
  LOAD key
  PUSH "!\n"
  PUSH 4
  CALL WRITE
  HALT
:game_over
  PUSH "Sorry, you missed it.\nThe number was: "
  LOAD key
  PUSH "\nTry it again!\n"
  PUSH 4
  CALL WRITE
  HALT