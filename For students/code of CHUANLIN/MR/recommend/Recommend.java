package recommand.hadoop.phl; 
import java.io.IOException; 
import java.net.URISyntaxException; 
import java.util.HashMap; 
import java.util.Map; 
import java.util.regex.Pattern; 
/** 
<ul><li>ÍÆ¼öÈë¿Ú</li> 
<li>@author root 
* 
*/ 
public class Recommend 
{ 
	public static final String HDFS = "hdfs://localhost:9000"; 
	public static final Pattern DELIMITER = Pattern.compile("[\t,]"); 
	public static void main(String[] args) throws ClassNotFoundException, IOException, URISyntaxException, InterruptedException 
	{ 
		Map<String,String> path = new HashMap<String,String>(); 
		path.put("Step1Input", HDFS + "/data/uItemTable.csv"); 
		path.put("Step1Output", HDFS + "/output/step1"); 
		path.put("Step2Input", path.get("Step1Output")); 
		path.put("Step2Output", HDFS + "/output/step2"); 
		path.put("Step3Input1", path.get("Step1Output")); 
		path.put("Step3Output1", HDFS + "/output/step3_1"); 
		path.put("Step3Input2", path.get("Step2Output")); 
		path.put("Step3Output2", HDFS + "/output/step3_2"); 
		path.put("Step4Input1", path.get("Step3Output1")); 
		path.put("Step4Input2", path.get("Step3Output2")); 
		path.put("Step4Output", HDFS + "/output/step4"); 
		Step1.runStep1(path); 
		Step2.runStep2(path); 
		Step3.runStep3_1(path); 
		Step3.runStep3_2(path); 
		Step4.runStep4(path); 
		System.exit(0); 
	} 
} 