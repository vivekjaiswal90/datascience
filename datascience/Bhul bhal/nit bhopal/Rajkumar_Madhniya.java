import java.io.*;
import jxl.*;
import jxl.write.*;
import java.util.*;

class ExcelRead
{
	 String c[]={"india","usa","uk","germany","australia","europe"};
	 String t[]={"ltd","co","org","sa","gesmbh","inc","llc","corp","bv","nv","corporation","sasu","gmbh","international"};

	ExcelRead()
	{
		try
		{
			Workbook wk=Workbook.getWorkbook(new File("Test_Project_NIT_Bhopal1.xls"));
			WritableWorkbook wr=Workbook.createWorkbook(new File("Test_Project_NIT_Bhopal1.xls"),wk);
			WritableSheet ws=wr.getSheet(0);
			Sheet st=wk.getSheet(0);
			Cell c;
			String s;
			Label l;
			for(int i=0;i<st.getRows();i++)
			{
				for(int j=0;j<st.getColumns();j++)
				{
					c=st.getCell(j,i);
					s=c.getContents();
					s=modify(s);
					l=new Label(j,i,s);
					ws.addCell(l);

				}
			}

			wr.write();
			wr.close();
			wk.close();

		}
		catch(Exception e)
		{
			System.out.println("Exception"+e);
		}
	}
	String modify(String str)
	{
		String r=null,a;
		int flag=0;
		StringTokenizer q;
		try
		{
	       q = new StringTokenizer(str,"-");
	       while (q.hasMoreTokens())
	        {
	    	   flag=0;
	           a=q.nextToken();
	           for(int i=0;i<6;i++)
	           {
	        	   if(c[i].equals(a))
	        		   flag=1;
	           }
	           if(flag==0)
	           {
	        	   	for(int i=0;i<13;i++)
	        	   	{
	        	   		if(t[i].equals(a))
	 	        		   flag=1;
	        	   	}
	           }
	           if(flag==0)
	           {
	        	  if(r==null)
	        		  r=a;
	        	  else
	        		  r+="-"+a;

	           }

	        }
		}
	  catch(Exception e)
	    {
		 System.out.println(e);
	    }
	  return r;

	}
	public static void main(String args[])
	{
		new ExcelRead();
	}
}
