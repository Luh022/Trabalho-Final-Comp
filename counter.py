#Contador

.START __main__

.DATA
    counter 5

.CODE

DEF __main__:
:while
  LOAD counter
  CMP 0
  JZ :after
  PUSH "\n"
  PUSH 2
  CALL WRITE
  LOAD counter
  PUSH 1
  SUB
  STOR counter
  JP :while
:after
  HALT