package recommand.hadoop.phl;

public class Cooccurrence 
{
    private int itemID1;
    private int itemID2;
    private int num;

    public Cooccurrence(int itemID1, int itemID2, int num) 
	{
        super();
        this.itemID1 = itemID1;
        this.itemID2 = itemID2;
        this.num = num;
    }

    public int getItemID1() 
	{
        return itemID1;
    }

    public void setItemID1(int itemID1) 
	{
        this.itemID1 = itemID1;
    }

    public int getItemID2() 
	{
        return itemID2;
    }

    public void setItemID2(int itemID2) 
	{
        this.itemID2 = itemID2;
    }

    public int getNum() 
	{
        return num;
    }

    public void setNum(int num) 
	{
        this.num = num;
    }

}