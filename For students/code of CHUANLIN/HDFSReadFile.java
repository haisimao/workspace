import java.io.BufferedReader;
import java.io.InputStreamReader;
import org.apache.hadoop.conf.Configuration;  
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.fs.FSDataInputStream;
public class HDFSReadFile
{
	public static void main(String[] args) 
	{
        try
        {
            Configuration conf = new Configuration();
			Path dfs=new Path("hdfs://localhost:9000/");
            FileSystem fs =dfs.getFileSystem(conf);
            Path filename = new Path("hdfs://localhost:9000/user/hadoop/test.txt");
            FSDataInputStream is = fs.open(filename);            
            BufferedReader d = new BufferedReader(new InputStreamReader(is));
            String content = d.readLine(); //��ȡ�ļ�һ�� 
            System.out.println(content);
            d.close(); //�ر��ļ� 
            fs.close(); //�ر�hdfs 
        } 
		catch(Exception e)
		{
			e.printStackTrace();
		}
    }  
}

