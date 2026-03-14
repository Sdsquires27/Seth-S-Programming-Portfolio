using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TilemapScript : MonoBehaviour
{
    [SerializeField] private List<Vector3Int> range1 = new List<Vector3Int>();
    [SerializeField] private List<Vector3Int> range2 = new List<Vector3Int>();
    [SerializeField] private List<Vector3Int> range3 = new List<Vector3Int>();
    [SerializeField] private List<Vector3Int> range4 = new List<Vector3Int>();

    public List<Vector3Int>[] placeables = new List<Vector3Int>[4];


    public List<Vector3Int> getVector3List(int listIndex)
    {
        placeables[0] = range1;
        placeables[1] = range2;
        placeables[2] = range3;
        placeables[3] = range4;

        List<Vector3Int> rangeList = placeables[listIndex];

        if (rangeList.Count == 2) // this feature automatically generates pieces in between two points if only two are given
        {
            if (rangeList[0].x != rangeList[1].x)
            {
                int firstX = rangeList[0].x; // the first x of the list
                int secondX = rangeList[1].x; // the second x of the list
                bool firstToSecond = firstX < secondX; // going from first to second or second to first
                for (int i = (firstToSecond ? firstX : secondX) + 1; i < (firstToSecond ? secondX : firstX); i++) // go from the smaller x to the larger x, incrementing by 1
                {
                    rangeList.Add(new Vector3Int(i, rangeList[0].y, rangeList[0].z));
                }
            }
            else
            {
                int firstY = rangeList[0].y; // the first y of the list
                int secondY = rangeList[1].y; // the second y of the list
                bool firstToSecond = firstY < secondY; // going from first to second or second to first
                for (int i = (firstToSecond ? firstY : secondY) + 1; i < (firstToSecond ? secondY : firstY); i++) // go from the smaller y to the larger y, incrementing by 1
                {
                    rangeList.Add(new Vector3Int(rangeList[0].x, i, rangeList[0].z));
                }
            }
        }
        return rangeList;
    }

    

    // Start is called before the first frame update
    void Start()
    {


    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
