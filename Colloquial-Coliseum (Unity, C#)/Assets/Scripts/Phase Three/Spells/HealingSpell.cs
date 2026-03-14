using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "Spell", menuName = "New Spell/Healing Spell")]
public class HealingSpell : Action
{
    public int spread;
    public bool aoe;

    public override string type
    {
        get
        {
            return "Healing";
        }
    }
    public override int size
    {
        get
        {
            return spread;
        }
    }

    public override bool targetsEnemy
    {
        get
        {
            return false;
        }
    }

    public override string description
    {
        get
        {
            return string.Format("{3}\nAMOUNT: {0}\nRANGE: {1}\nSPREAD: {2}\nRECHARGE: {4}", damage, range, size, name.ToUpper(), rechargeTime);
        }
    }

    public override bool isAoe
    {
        get
        {
            return aoe;
        }
    }

    public override int chanceToHit(Unit enemy)
    {
        throw new System.NotImplementedException();
    }

    public override void use(TileObject tileToAffect, PlayerController playerController)
    {
        tileToAffect.heal(damage);
        timeRecharging = rechargeTime;
    }

    public override void use(Vector3Int tileToAffect, PlayerController curPlayer)
    {
        Debug.Log("Aoe spell used");
        foreach (TileObject tileObject in LevelScript.objectsInTiles(LevelScript.tilesInRange(tileToAffect, range)))
        {

            // don't deal healing to own player
            if (tileObject.playerController == curPlayer)
            {
                tileObject.heal(damage);
            }

        }
    }
}