//import org.apache.hadoop.conf.Configuration;
//import org.apache.hadoop.fs.FileSystem;
//import org.apache.hadoop.fs.Path;
//public class HDFSFileifExist 
//{
//	public static void main(String[] args)
//	{
//		try
//		{
//			String fileName="hdfs://localhost:9000/user/hduser/hfile";
//			Configuration conf = new Configuration();
//			conf.set("fs.default.name", "hdfs://localhost:9000");
//			conf.set("fs.hdfs.impl", "org.apache.hadoop.hdfs.DistributedFileSystem");
//			FileSystem fs = FileSystem.get(conf);
//			if(fs.exists(new Path(fileName)))
//			{
//					System.out.println("File existed");
//			}
//			else
//			{
//				System.out.println("File dose not exist");
//			}
//		}
//		catch(Exception e)
//		{
//			e.printStackTrace();
//		}
//	}
//}
class Person{
 String name ;
 String city ;
 int age ;
 public Person(String name, String city, int age)
{
 this.name = name ;
 this.city = city ;
 this.age = age ;
}
 public String talk()
{
 return "我是："+this.name+"，今年："+this.age+"岁，来自："+this.city;
}
}
 public class HDFSFileifExist
{
 public static void main(String[] args)
{
 Person p1 = new Person("张三",25,"中国") ;
 Person p2 = new Person("李四",30,"中国") ;
 Person p3 = new Person("王五",35,"中国") ;
 System.out.println(p1.talk()) ;
 System.out.println(p2.talk()) ;
 System.out.println(p3.talk()) ;
}
  }
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 