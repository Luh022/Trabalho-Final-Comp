#Calculo da Area

.START __main__

.DATA
    pi   3.141592

.CODE

DEF __main__:
  PUSH "Ray: "
  PUSH 1
  CALL WRITE
  CALL READ
  DUP
  MUL
  LOAD pi
  MUL
  PUSH "\n"
  PUSH 2
  CALL WRITE
  HALT