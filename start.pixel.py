.START __main__

.INIT 0 0 200 200

.DATA
    counter 200

.CODE

DEF random_0_100:
  PUSH 200
  RAND
  MUL
  TRUNC
  RET

DEF __main__:
:while
  # while counter > 0
  LOAD counter
  CMP 0
  JZ :after
  # x = random [0;200)
  CALL random_0_200
  # y = random [0;200)
  CALL random_0_200
  # desenho no (x,y)
  MVTO
  SETPX
  # contador -= 2
  LOAD counter
  PUSH 2
  SUB
  STOR counter
  # próxima interação
  JP :while
:after
  HALT