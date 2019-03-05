package recommand.hadoop.phl; 
import java.io.IOException; 
import java.net.URI; 
import java.net.URISyntaxException; 
import org.apache.hadoop.conf.Configuration; 
import org.apache.hadoop.fs.FileSystem; 
import org.apache.hadoop.fs.Path; 
import org.apache.hadoop.mapreduce.Job; 
import sun.tools.tree.ThisExpression; 
public class HDFSDao
{ 
//HDFS���ʵ�ַ 
	private static final String HDFS = "hdfs://localhost:9000/"; 
//hdfs·�� 
	private String hdfsPath; 
//Hadoopϵͳ���� 
	private Configuration conf; 
//����job������ 
	private String name; 
	public HDFSDao(Configuration conf)
	{ 
		this.conf = conf; 
	} 
	public HDFSDao( Configuration conf,String name) 
	{ 
		this.conf = conf; 
		this.name = name; 
	} 
	public HDFSDao(String hdfs, Configuration conf,String name) 
	{ 
		this.hdfsPath = hdfs; 
		this.conf = conf; 
		this.name = name; 
	} 
	public Job conf() throws IOException
	{ 
		Job job = Job.getInstance(this.conf,this.name); 
		return job; 
	} 
	public void rmr(String outUrl) throws IOException, URISyntaxException 
	{ 
		FileSystem fileSystem = FileSystem.get(new URI(outUrl),this.conf); 
		if(fileSystem.exists(new Path(outUrl)))
		{ 
			fileSystem.delete(new Path(outUrl), true); 
			System.out.println("outUrl "+outUrl); 
		} 
	} 
} 