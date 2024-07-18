

```
struct {
   type [member_name] : width ;
};
```

|Element    | Description
|-          | - 
|type       | An integer type that determines how a bit-field's value is interpreted.The type may be int, signed int, or unsigned int.只能是整型数据类型
|member_name| The name of the bit-field.
|width	    | Number of bits in the bit-field. "width" must be less than or equal to bit width of specified type. Bit fields can range in size from 1 to 64 bits in C or larger in C++. The maximum bit-field length is 64 bits. To increase portability, do not use bit fields greater than 32 bits in size.



1. 在C中，位域的数据类型一律用无符号的
2. 可以有空域，匿名域，0表示该类型后面位不使用，非零值表示跳过这几位填充
3. 如果一个位域的位的分配超过了该类型的位的总数，则从下一个单元开始继续分配，这个很好理解：


位域的使用主要出现在如下两种情况:
 (1)当机器可用内存空间较少而使用位域可以大量节省内存时。如,当把结构作为大数组的元素时。
 (2)当需要把一结构或联合映射成某预定的组织结构时。例如,当需要访问字节内的特定位时。
If storage is limited, we can go for bit-field.
When devices transmit status or information encoded into multiple bits for this type of situation bit-field is most efficient.
Encryption routines need to access the bits within a byte in that situation bit-field is quite useful.


当要把某个成员说明成位域时,其类型只能是int,unsigned int与signed int三者之一(说明:int类型通常代表特定机器中整数的自然长度。short类型通常为16位,long类型通常为32位,int类型可以为16位或32位.各编译器可以根据硬件特性自主选择合适的类型长度.

关于位域还需要提醒读者注意如下几点:
其一,位域的长度不能大于int对象所占用的字位数.例如,若int对象占用16位,则如下位域说明是错误的:
     unsigned int x:17;
其二,由于位域的实现会因编译程序的不同而不同,在此使用位域会影响程序的可移植性,在不是非要使用位域不可时最好不要使用位域.
其三,尽管使用位域可以节省内存空间,但却增加了处理时间,在为当访问各个位域成员时需要把位域从它所在的字中分解出来或反过来把一值压缩存到位域所在的字位中.
其四,位域的位置不能访问,因些不能对位域使用地址运算符号&(而对非位域成员则可以使用该运算符).从而,即不能使用指向位域的旨针也不能使用位域的数组(因为数组实际上就是一种特殊的指针).另外,位域也不能作为函数返回的结果.
最后还要强调一遍:位域又叫位段(位字段),是一种特殊的结构成员或联合成员(即只能用在结构或联合中).

[C语言：--位域和内存对齐-腾讯云开发者社区-腾讯云](https://cloud.tencent.com/developer/article/1784615)  关于内存对齐，结合数据解析程序的例子。单独成文。
[Bit Fields in C](https://www.tutorialspoint.com/cprogramming/c_bit_fields.htm)
[Bit Fields in C - GeeksforGeeks](https://www.geeksforgeeks.org/bit-fields-c/)
[downloads.ti.com/docs/esd/SPRUI04/bit-fields-stdz0545438.html](https://downloads.ti.com/docs/esd/SPRUI04/bit-fields-stdz0545438.html




位域(位段)

位域类型可以是整数（可以是cv限定const, volatile）或枚举类型，匿名位域不能是cv限定类型。

[Bit-field - cppreference.com](https://en.cppreference.com/w/cpp/language/bit_field)
[Arm Compiler for Embedded User Guide](https://developer.arm.com/documentation/100748/0619/Writing-Optimized-Code/Packing-data-structures)
[IBM Documentation - IBM Documentation](https://www.ibm.com/docs/en/xcafbg/9.0.0?topic=SS3KZ4_9.0.0/com.ibm.xlcpp9.bg.doc/proguide/calgnbit.html)

[IBM Documentation - IBM Documentation](https://www.ibm.com/docs/en/i/7.1?topic=declarations-bit-field-members)
[Flexible array members - IBM Documentation](https://www.ibm.com/docs/en/i/7.5?topic=declarations-flexible-array-members)