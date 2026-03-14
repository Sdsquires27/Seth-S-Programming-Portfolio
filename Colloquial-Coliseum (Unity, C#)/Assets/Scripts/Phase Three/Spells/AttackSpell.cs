using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[CreateAssetMenu(fileName = "Spell", menuName = "New Spell/Attack Spell")]
public class AttackSpell : Action
{

    public override string type
    {
        get
        {
            return "Attack";
        }
    }

    public override int size
    {
        get
        {
            return 0;
        }
    }
    public override bool targetsEnemy
    {
        get
        {
            return true;
        }
    }
    public override bool isAoe
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
            return string.Format("{2}\nDAMAGE: {0}\nRANGE: {1}\nRECHARGE: {3}", damage, range, name.ToUpper(), rechargeTime);
        }
    }

    public override int chanceToHit(Unit enemy)
    {
        return 100 - enemy.armor * 7;
    }

    public override void use(TileObject tileToAffect, PlayerController playerController)
    {
        int rand = Random.Range(0, 100);

        if (tileToAffect.unit.armor * 7 <= rand)
        {
            tileToAffect.takeDamage(damage, playerController);
            hitMessage(new Unit[] { tileToAffect.unit }, damage, Color.green);
        }
        else
        {
            hitMessage(new Unit[] { tileToAffect.unit }, 0, Color.red);

        }
        timeRecharging = rechargeTime;
    }

    public override void use(Vector3Int tileToAffect, PlayerController playerController)
    {
        throw new System.NotImplementedException();
    }
}