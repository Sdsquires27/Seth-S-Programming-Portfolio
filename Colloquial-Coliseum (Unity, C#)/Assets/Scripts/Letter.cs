using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "Letter", menuName = "New Letter")]
public class Letter: ScriptableObject
{
    public char character;
    public int worth;
    public int amount;
    public Sprite sprite;
}
