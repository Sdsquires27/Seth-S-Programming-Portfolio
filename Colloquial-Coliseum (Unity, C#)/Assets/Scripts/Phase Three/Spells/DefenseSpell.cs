using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "Spell", menuName = "New Spell/DefenseSpell")]
public class DefenseSpell : Action
{
    public int defense;

    public override string type
    {
        get
        {
            return "Defense";
        }
    }
    public override int size
    {
        get
        {
            return 0;
        }
    }

    public override string description
    {
        get
        {
            return string.Format("{3}\nSHIELD: {0}\nRANGE: {1}\nSPREAD: {2}\nTHORNS: {4}\nRECHARGE: {5}", defense, range, size, name.ToUpper(), damage, rechargeTime);
        }
    }

    public override bool targetsEnemy
    {
        get
        {
            return false;
        }
    }

    public override bool isAoe
    {
        get
        {
            return false;
        }
    }

    public override int chanceToHit(Unit enemy)
    {
        throw new System.NotImplementedException();
    }

    public override void use(TileObject tileToAffect, PlayerController curPlayer)
    {
        tileToAffect.giveDefense(defense, damage);
        timeRecharging = rechargeTime;
    }
    public override void use(Vector3Int tileToAffect, PlayerController playerController)
    {
        throw new System.NotImplementedException();
    }
}
