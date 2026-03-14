using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class WordTileHandler : MonoBehaviour
{
    [SerializeField] private List<UIWorldTileScript> firstTiles;
    [SerializeField] private List<UIWorldTileScript> secondTiles;
    [SerializeField] private int secondIndex;
    private int firstIndex = 0;
    public string word;

    private void Start()
    {
        bool foundIndex = false;
        foreach(Transform obj in transform)
        {
            if (obj.parent.transform != transform) return;
            if (obj.TryGetComponent(out UIWorldTileScript tile))
            {
                firstTiles.Add(tile);
            }
            else
            {
                foundIndex = true;
                
                foreach(Transform obj2 in obj.GetChild(0).transform)
                {
                    if (obj2.parent.transform != obj.GetChild(0).transform) return;
                    UIWorldTileScript tile2 = obj2.GetComponent<UIWorldTileScript>();
                    secondTiles.Add(tile2);
                }
            }
            if (!foundIndex) firstIndex++;
        }

        firstTiles.Insert(firstIndex, secondTiles[secondIndex]);
        
    }

    private string curWord()
    {
        string ret = "";

        foreach(UIWorldTileScript tile in firstTiles)
        {
            ret += tile.curState;
        }
        foreach(UIWorldTileScript tile in secondTiles)
        {
            ret += tile.curState;
        }

        return ret;
    }

    private void Update()
    {
        word = curWord();
    }


}
