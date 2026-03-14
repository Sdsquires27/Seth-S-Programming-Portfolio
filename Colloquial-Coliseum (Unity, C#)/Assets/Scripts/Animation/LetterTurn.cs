using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LetterTurn : MonoBehaviour
{
    // script for turning a letter on a tile

    // time for the turning animation to play
    public float timeToTurn;

    // Start is called before the first frame update
    void Start()
    {
        StartCoroutine(rotate(timeToTurn));  
    }

    private IEnumerator rotate(float turnTime)
    {
        // repeat the small turn equal to the time in milliseconds it takes
        for (int i = 0; i < turnTime; i++)
        {
            // turn the tile
            transform.Rotate(new Vector3(0, 90 / timeToTurn, 0));

            // wait
            yield return new WaitForSeconds(.005f);

        }
        Debug.Log(Time.fixedTime);

    }

    // Update is called once per frame
    void FixedUpdate()
    {
/*        transform.Rotate(new Vector3(0, 90 / timeToTurn, 0));
        Debug.Log(transform.rotation.y);*/
    }
}
