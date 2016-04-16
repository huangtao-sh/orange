# Xlsx报表库
# 主要是对xlsxwriter进行进一步封装
# 作者：黄涛
# 创建：2015-12-04

from xlsxwriter.utility import xl_col_to_name
from xlsxwriter import Workbook
from xlsxwriter.worksheet import convert_range_args

# 预定义格式
DefaultFormats=(('currency',{'num_format':'#,##0.00'}),
                ('rate',{'num_format':'0.0000%'}),
                ('percent',{'num_format':'0.00%'}),
                ('date',{'num_format':'yyyy-mm-dd'}),
                ('time',{'num_format':'hh:mm:ss'}),
                ('datetime',{'num_format':'yyyy-mm-dd hh:mm:ss'}),
                ('timestamp',{'num_format':'yyyy-mm-dd hh:mm:ss.0'}))

class XlsxReport():
    def __init__(self,*args,**kwargs):
        self.book=Workbook(*args,**kwargs)
        self.formats={}
        self.add_formats(DefaultFormats)
        
    def close(self):
        self.book.close()

    def add_formats(self,args):
        if isinstance(args,dict):
            args=args.items()
        self.formats.update({name:self.book.add_format(format) for \
                    name,format in args})
                      
    @convert_range_args
    def add_table(self,first_row,first_col,last_row,last_col,\
                  sheetname,**kwargs):
        sheet=self.book.add_worksheet(sheetname)
        columns=kwargs.get('columns')
        if columns:
            new_columns=[]
            for idx,column in enumerate(columns):
                if 'width' in column:
                    sheet.set_column("{0}:{0}".format(
                        xl_col_to_name(idx+first_col)),\
                        column.get('width'))
                format=column.get("format")
                if format and isinstance(format,str):
                    new_column=column.copy()
                    new_column['format']=self.formats.get(format)
                    new_columns.append(new_column)
                else:
                    new_columns.append(column)

            kwargs['columns']=new_columns
            last_col=first_col+len(columns)-1
        if 'data' in kwargs:
            last_row=first_row+len(kwargs['data'])
            if kwargs.get('total_row',False):
                last_row+=1
        sheet.add_table(first_row,first_col,last_row,last_col,kwargs)
                
