# BIPDecoder
**Image decoder for PS2 BIP format**  
## Announcement
当前此脚本落后于修改进度，不推荐使用此脚本，请先尝试使用[GARbro-Mod-1.0.1.2E20](https://github.com/Manicsteiner/GARbro/releases/tag/GARbro-Mod-1.0.1.2E20)或更高版本。  
## Usage
首先获取PS2游戏的ISO镜像，从中提取出BG.AFS和EV.AFS。用GARBro打开AFS文件，提取出其中的BIP文件。将BIP文件的内容作为LZSS Stream解压（可以修改后缀名为spc，用GARbro打开），得到解压缩后的文件。  
将该文件拖放至BIPDecoder.py上。  
~~_I-O_(SLPM-66272)请使用BIP-r32，_Remember11_(SLPM-65550)请使用BIP-r16。这种区别应当可以从文件中读取，有待继续研究。已解决~~  
可能适用的游戏：[BIP-T2P](https://manicsteiner.github.io/blog/20231101-ps2cri/index.html#BIP-T2P)  
运行脚本需要安装python3，pillow。  

BIP-r64当前为_Kono Ozora ni Tsubasa o Hirogete Cruise Sign_(BLJM61184)的ev.cpk之中的文件测试使用，未加入GARbro。  