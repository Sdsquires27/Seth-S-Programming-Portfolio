using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class LetterFollow : MonoBehaviour
{
    float lerpTime = 1f;
    float curLerpTIme;

    [System.NonSerialized] public Transform toFollow;

    Vector2 startPos;
    Vector2 endPos;

    public WordTileScript wordTile;

    bool lerping = false;

    private void Start()
    {
        
    }

    public void teleport()
    {
        //should teleport.
        transform.position = toFollow.position;
        curLerpTIme = 0f;
        lerping = false;
    }

    // Update is called once per frame
    void Update()
    {
        if (!lerping)
        {
            if (toFollow.position != transform.position)
            {
                endPos = toFollow.position;
                startPos = transform.position;
                lerping = true;
                curLerpTIme = 0;
            }
        } 

        else
        {
            if(endPos != (Vector2)toFollow.position)
            {
                curLerpTIme = 0;
                endPos = (Vector2)toFollow.position;
                startPos = transform.position;
            }

            curLerpTIme += Time.deltaTime;
            if (curLerpTIme > lerpTime)
            {
                curLerpTIme = lerpTime;
                lerping = false;
            }

            float t = curLerpTIme / lerpTime;
            t = t * t * t * (t * (6f * t - 15f) + 10f);
            transform.position = Vector3.Lerp(startPos, endPos, t);
        }
    }
}
