"""
First we get the target function and access the mlil of it

Next we want to create an array of bytes we are interested in to decode

We can loop through the instructions and look specifically for the "var_94"
(Note: Prior to this we had to set that variable to a char array. This can 
be done by putting your cursor on the variable (in this case var_94), pressing
"Y" on the keyboard to change the type and then setting it to "char var_94[0x80]" 

Each instruction in mlil is given a tuple of operands. We are looking for when that is 3
in this sample (and maybe in general but not sure yet) a single operand we are interested in looks
like this:

[('dest', <var char str_bytes[0x80]>, 'Variable'), ('offset', 0, 'int'), ('src', <MediumLevelILConst: 1>, 'MediumLevelILInstruction')]

What we are interested in in the list above are the offset and the value being set. Based on the decryption
we only care about odd offsets (due to the modulo 2).

the loop puts the bytes into 
the "<class 'binaryninja.mediumlevelil.MediumLevelILConst'>" object so 
we can convert those to integers.

Getting the value results in 
"<class 'binaryninja.variable.ConstantRegisterValue'>". This class
also has a value property so the resulting data we want for each object
is in the "object".value.value property

Additionally we can do the XOR of 0x55 on each character we want. First we
set encoded and decoded string variables and then loop through the bytes. The
"enc" just gets the byte written and the "dec" gets the byte with the XOR
"""

target_function = bv.get_function_at(0x401000)
mlil_target_function = target_function.mlil

bytes = []
for i in mlil_target_function.instructions:
    if len(i.detailed_operands) == 3:
        if isinstance(i.detailed_operands[0][1],binaryninja.variable.Variable):
            if i.detailed_operands[0][1].name == 'str_bytes':
                offset = i.detailed_operands[1][1]
                if offset % 2 == 1:
                    bytes.append(i.detailed_operands[2][1])

enc = ''
dec = ''
for i in bytes:
    enc += chr(i.value.value)
    dec += chr(i.value.value ^ 0x55)

print(f"Encoded string: {enc}")
print(f"Decoded string: {dec}")