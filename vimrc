"==================================
"    Vim基本配置
"===================================
"设置GUI相关属性
set guifont=AR\ PL\ UKai\ CN\ 12
"设置标签栏是否显示
if has('gui_running')
    set showtabline=2
else
    set showtabline=0
endif

"关闭vi的一致性模式 避免以前版本的一些Bug和局限
set nocompatible
"配置backspace键工作方式
set backspace=indent,eol,start

"显示行号
set nu
"设置在编辑过程中右下角显示光标的行列信息
set ru
"当一行文字很长时取消换行
"set nowrap

"在状态栏显示正在输入的命令
set showcmd

"设置历史记录条数
set history=1000

"设置取消备份 禁止临时文件生成
set nobackup
set noswapfile

"高亮搜索结果
set hlsearch

"突出显示当前行列
set cursorline
"set cursorcolumn

"设置匹配模式 类似当输入一个左括号时会匹配相应的那个右括号
set showmatch

"设置C/C++方式自动对齐
set autoindent
set cindent

"开启语法高亮功能
syntax enable
syntax on

"指定配色方案为256色
set t_Co=256

"设置搜索时忽略大小写
set ignorecase

"设置在Vim中可以使用鼠标 防止在Linux终端下无法拷贝
set mouse=a

"设置Tab宽度
set tabstop=4
"设置自动对齐空格数
set shiftwidth=4
"设置按退格键时可以一次删除4个空格
set softtabstop=4
"设置按退格键时可以一次删除4个空格
set smarttab
"将Tab键自动转换成空格 真正需要Tab键时使用[Ctrl + V + Tab]
set expandtab

"设置编码方式
set encoding=utf-8
"自动判断编码时 依次尝试一下编码
set fileencodings=ucs-bom,utf-8,cp936,gb18030,big5,euc-jp,euc-kr,latin1

"检测文件类型
filetype on
"针对不同的文件采用不同的缩进方式
filetype indent on
"允许插件
filetype plugin on
"启动智能补全
filetype plugin indent on

"Vundle配置
set nocompatible
filetype off
set rtp+=~/.vim/bundle/vundle/
call vundle#rc()
"let vundle manage vundle
Bundle 'gmarik/vundle'

"vim-scripts repos
Bundle 'L9'
Bundle 'taglist.vim'

"original repos on github
Bundle 'altercation/vim-colors-solarized'
Bundle 'scrooloose/nerdtree'
Bundle 'vim-scripts/OmniCppComplete'
Bundle 'jiangmiao/auto-pairs'

"non github repos

"NERDTree
"autocmd vimenter * NERDTree
map <F2> :NERDTreeToggle<CR>
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTreeType") && b:NERDTreeType == "primary") | q | endif

"taglist
let Tlist_Auto_Open=1        "启动VIM后自动打开
let Tlist_Show_Menu=1
let Tlist_Show_One_File=1    "只显示当前文件的tags
let Tlist_WinWidth=40        "设置taglist宽度
let Tlist_Exit_OnlyWindow=1  "tagList窗口是最后一个窗口，则退出Vim
let Tlist_Use_Right_Window=1 "在Vim窗口右侧显示taglist窗口
let Tlist_Use_SingleClick=1  "使能单击选中

"auto-pairs
"let g:AutoPairsFlyMode=1

"solarized
syntax enable
if has('gui_running')
    set background=dark
else
    set background=dark
endif
let g:solarized_termcolors=256
let g:solarized_termtrans=0
colorscheme solarized
