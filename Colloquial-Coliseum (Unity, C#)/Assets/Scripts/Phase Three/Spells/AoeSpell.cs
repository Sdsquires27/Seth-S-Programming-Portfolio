using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "Spell", menuName = "New Spell/Aoe Spell")]
public class AoeSpell : Action
{

    public int spread;

    public override string type
    {
        get
        {
            return "AoE";
        }
    }
    public override bool targetsEnemy
    {
        get
        {
            return true;
        }
    }

    public override int size
    {
        get
        {
            return spread;
        }
    }


    public override bool isAoe
    {
        get
        {
            return true ;
        }
    }

    public override string description
    {
        get
        {
            return string.Format("{3}\nDAMAGE: {0}\nRANGE: {1}\nSPREAD: {2}\nRECHARGE: {4}", damage, range, size, name.ToUpper(), rechargeTime);
        }
    }

    [System.NonSerialized] public Vector3Int[] rangeTiles;

    public override void use(TileObject tileToAffect, PlayerController playerController)
    {
        throw new System.NotImplementedException();
    }

    public override void use(Vector3Int startTile, PlayerController playerController)
    {
        Debug.Log("Action being used");
        foreach(Vector3Int tile in LevelScript.tilesInRange(startTile, spread))
        {
            Debug.Log(tile);
        }
        foreach (TileObject tileObject in LevelScript.objectsInTiles(LevelScript.tilesInRange(startTile, spread)))
        {
            Debug.Log(tileObject.unit.word);
            // don't deal damage to own player
            Debug.Log(playerController.color.r);
            Debug.Log(tileObject.playerController.color.r);
            if (tileObject.playerController != playerController) 
            {
                Debug.Log("Is not the same player");
                int rand = Random.Range(0, 100);

                if (tileObject.unit.armor * 7 <= rand)
                {
                    Debug.Log("Hit");
                    tileObject.takeDamage(damage, playerController);
                    hitMessage(new Unit[] { tileObject.unit }, damage, Color.blue);
                }
                else
                {
                    Debug.Log("Did not hit");
                    hitMessage(new Unit[] { tileObject.unit }, 0, Color.red);

                }
            }
            else
            {
                Debug.Log("Is the same player");

            }

        }
    }

    public override int chanceToHit(Unit enemy)
    {
        return (100 - enemy.armor * 7);
    }
}
