# Desenhando um retângulo

.START __main__

.INIT 0 4 20 20

.DATA
  square_length_p 0

.CODE

DEF __main__:
  PUSH 10
  CALL square
  PUSH 40
  PUSH 14
  CALL MOVE
  HALT


DEF square:
  STOR square_length_p
  PUSH 0
  LOAD square_length_p
  CALL MOVE
  PUSH 90
  LOAD square_length_p
  CALL MOVE
  PUSH 180
  LOAD square_length_p
  CALL MOVE
  PUSH 270
  LOAD square_length_p
  CALL MOVE
  RET