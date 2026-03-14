using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public abstract class Action : ScriptableObject, IInfoPanel
{
    [System.NonSerialized]
    public int timeRecharging;

    public int rechargeTime;
    public int range;
    public int damage;

    public abstract string type { get; }

    public abstract int size { get; }

    public abstract int chanceToHit(Unit enemy);


    // does the action attack enemies or benefit allies?
    public abstract bool targetsEnemy { get; }
    public abstract bool isAoe { get; }
    public abstract string description { get; }


    // what tiles does the attack affect?
    public abstract void use(TileObject tileToAffect, PlayerController curPlayer);

    public abstract void use(Vector3Int startTile, PlayerController curPlayer);

    public void hitMessage(Unit[] unitsHit, int damage, Color color)
    {
        foreach(Unit unit in unitsHit)
        {
            GameManager.displayMessage("HIT '" + unit.word + "' FOR " + damage + " DAMAGE", color) ;
        }
    }


    public string filePath()
    {
        return "Sprites/Spells/Icons/" + type + "/" + name;
    }

    public void reduceChargeTime()
    {
        if(timeRecharging > 0)
        {
            timeRecharging--;
        }
    }




    public class Attack : Action
    {
        int piercing;
        TileObject owner;

        public Attack()
        {
            this.name = "Attack";
        }
        public Attack(int range, int piercing, int damage)
        {
            this.name = "Attack";
            this.range = range;
            this.piercing = piercing;
            this.damage = damage;
        }

        public Attack(Unit unit, TileObject owner)
        {
            this.name = "Attack";
            this.range = unit.range;
            this.piercing = unit.piercing;
            this.damage = unit.dmg;
            this.owner = owner;
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
                return 0;
            }
        }
        public override bool isAoe
        {
            get
            {
                return false;
            }
        }


        public override string type
        {
            get
            {
                return "Attack";
            }
        }

        public override string description
        {
            get
            {
                return string.Format("{3}\nDAMAGE: {0}\nRANGE: {1}\nPIERCING: {2}", damage, range, piercing, name.ToUpper());
            }
        }

        public override int chanceToHit(Unit enemy)
        {
            return 100 - (enemy.armor * 15) + (piercing * 15);
        }

        public override void use(TileObject toAttack, PlayerController player)
        {
            int rand = Random.Range(0, 100);
            rand += piercing * 15;
            if (toAttack.unit.armor * 15 <= rand)
            {
                toAttack.takeDamage(damage, player);
                hitMessage(new Unit[] { toAttack.unit }, damage, Color.green);
            }
            else
            {
                hitMessage(new Unit[] { toAttack.unit }, 0, Color.red);

            }
            if(toAttack.thorns > 0)
            {
                owner.takeDamage(toAttack.thorns, toAttack.playerController);
            }

        }
        
        public override void use(Vector3Int tileToAttack, PlayerController curPlayer)
        {

        }


    }
}
   
