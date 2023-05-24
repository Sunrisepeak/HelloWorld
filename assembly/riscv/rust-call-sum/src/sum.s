# 1 + ... + n - 1
.text
    .align 2
    
    # Function to compute sum of numbers from 1 to n
sum:
    addi    sp, sp, -16      # make room for 4 values on the stack
    sw      ra, 0(sp)        # store return address
    sw      s0, 4(sp)        # store s0
    sw      s1, 8(sp)        # store s1
    sw      s2, 12(sp)       # store s2

    li      t3, 0            # initialize sum to zero
    li      t4, 1            # initialize i to 1
    add     t5, a0, 1        # end condition

loop:
    beq     t4, t5, done     # if i == n + 1, exit loop
    add     t3, t3, t4       # add i to sum
    addi    t4, t4, 1        # increment i
    j       loop             # jump to loop

done:
    mv      a0, t3           # move sum to a0
    lw      ra, 0(sp)        # restore return address
    lw      s0, 4(sp)        # restore s0
    lw      s1, 8(sp)        # restore s1
    lw      s2, 12(sp)       # restore s2
    addi    sp, sp, 16       # restore stack pointer
    jr      ra               # return to the calling function