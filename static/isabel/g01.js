var player, field, ball, cursorKeys, pointer, flag = false; endgame = false;
var velocity = 200;
var gwidth = 3027 / 2.55, gheight = 2000 / 2.5;
var scoreText, score0 = 0, score1 = 0, finalText;
var config = {
    type: Phaser.AUTO,
    width: gwidth,
    height: gheight,
    physics: {
        default: 'arcade',
        arcade: {
            //gravity: { y: 300 },
            debug: false
        }
    },
    scene: {
        preload: preload,
        create: create,
        update: update
    },
    scale: {
        mode: Phaser.Scale.FIT,
        autoCenter: Phaser.Scale.CENTER_BOTH
    }
};

var game = new Phaser.Game(config);

function preload() {
    this.load.image('field', '/static/isabel/assets/field1.png');
    this.load.image('ball', '/static/isabel/assets/ball1.png');
    this.load.image('player', '/static/isabel/assets/player.png');
    this.load.image('plRight1', '/static/isabel/assets/player2.png');
    this.load.image('plRight2', '/static/isabel/assets/player2.png');
    this.load.image('goalKeeperRight', '/static/isabel/assets/player2.png');
    this.load.image('gates', '/static/isabel/assets/gates.png');
}

function create() {
    field = this.add.image(gwidth / 2 + 3, gheight / 2, 'field');
    gatesL = this.physics.add.image(2, 400, 'gates');
    gatesR = this.physics.add.image(1183, 400, 'gates');
    scoreText = this.add.text(gwidth / 2 - 72, 16, ' 0', { fontSize: '48px', fill: '#FFF' });
    finalText = this.add.text(gwidth / 8, 160, '', { fontSize: '48px', fill: '#FFF' });
    ball = this.physics.add.image(gwidth / 2, gheight / 2, 'ball');
    player = this.physics.add.image(120, 120, 'player');
    plLeft2 = this.physics.add.image(120, 680, 'player');
    goalKeeperLeft = this.physics.add.image(32, 313, 'player');
    plRight1 = this.physics.add.image(1120, 120, 'plRight1');
    plRight2 = this.physics.add.image(1120, 620, 'plRight2');
    goalKeeperRight = this.physics.add.image(1150, 330, 'goalKeeperRight');

    gatesL.setScale(1.6);
    gatesR.setScale(1.6);
    player.setScale(0.4);
    plLeft2.setScale(0.4);
    goalKeeperLeft.setScale(0.4);
    plRight1.setScale(0.4);
    plRight2.setScale(0.4);
    goalKeeperRight.setScale(0.4);

    ball.setScale(0.7);
    //field.setScaleY(0.5);
    field.setScale(0.418);

    cursorKeys = this.input.keyboard.createCursorKeys();
    this.input.mouse.capture = true;
    // pointer = this.input.pointer.

    player.setCollideWorldBounds(true);
    plLeft2.setCollideWorldBounds(true);
    goalKeeperLeft.setCollideWorldBounds(true);
    player.setBounce(0);
    plLeft2.setBounce(0);
    goalKeeperLeft.setBounce(0);

    plRight1.setCollideWorldBounds(true);
    plRight2.setCollideWorldBounds(true);
    goalKeeperRight.setCollideWorldBounds(true);
    plRight1.setBounce(1);
    plRight2.setBounce(1);
    goalKeeperRight.setBounce(0);
    // plRight1.setVelocityX(Math.random() * velocity * 0.5 *
    //     ((Math.random() > 0.5)? 1: -1)
    //     );
    // plRight1.setVelocityY(Math.random() * velocity * 0.5*
    //     ((Math.random() > 0.5)? 1: -1)
    // );
    // plRight2.setVelocityX(Math.random() * velocity * 0.5 *
    //     ((Math.random() > 0.5)? 1: -1)
    //     );
    plRight1.setVelocityX(Phaser.Math.Between(-150, 150));
    plRight1.setVelocityY(Phaser.Math.Between(-150, 150));
    plRight2.setVelocityX(Phaser.Math.Between(-150, 150));
    plRight2.setVelocityY(Phaser.Math.Between(-150, 150));
    // plRight2.setVelocityY(Math.random() * velocity * 0.5*
    //     ((Math.random() > 0.5)? 1: -1)
    // );
    goalKeeperRight.setVelocityY(Math.random() * velocity * 0.5 *
        ((Math.random() > 0.5) ? 1 : -1)
    );
    goalKeeperLeft.setVelocityY(Math.random() * velocity * 0.5 *
        ((Math.random() > 0.5) ? 1 : -1)
    );


    ball.setVelocityX(Math.random() * velocity * 1.3 *
        ((Math.random() > 0.5) ? 1 : -1)
    );
    ball.setVelocityY(Math.random() * velocity * 1.3 *
        ((Math.random() > 0.5) ? 1 : -1)
    );

    ball.setCollideWorldBounds(true);
    ball.setBounce(1);

    this.physics.add.collider(player, ball, hittheball11, null, this);
    this.physics.add.collider(plLeft2, ball, hittheball12, null, this);
    this.physics.add.collider(goalKeeperLeft, ball, hittheball10, null, this);
    this.physics.add.collider(plRight1, ball, hittheball21, null, this);
    this.physics.add.collider(plRight2, ball, hittheball22, null, this);
    this.physics.add.collider(plRight1, player, collideMan1, null, this);
    this.physics.add.collider(plRight2, plLeft2, collideMan2, null, this);
    this.physics.add.collider(goalKeeperRight, ball, hittheball20, null, this);
    this.physics.add.overlap(gatesL, ball, goalLeft, null, this);
    this.physics.add.overlap(gatesR, ball, goalRight, null, this);
    player.setBounce(0, 0);
    plLeft2.setBounce(0, 0);

    this.physics.moveTo(plRight1, ball.x, ball.y, 150, 3000);
    this.physics.moveTo(plRight2, ball.x, ball.y, 150, 3000);


    this.input.on('pointerdown', function (pointer) {

        //this.input.mouse.requestPointerLock();
        this.physics.moveTo(player, pointer.x, pointer.y, 200);
        this.physics.moveTo(plLeft2, pointer.x, pointer.y, 200);
        //console.log("x: " + pointer.x + "   y: " + pointer.y);
        if (!flag) {
            flag = true;
        }


    }, this);
    // this.input.on('pointermove', function (pointer) {

    //     if (this.input.mouse.locked)
    //     {
    //                 this.input.mouse.releasePointerLock();
    //     }
    // }, this);
}

function update() {
    if (!flag) {

        player.setVelocityX(0);
        player.setVelocityY(0);
        plLeft2.setVelocityX(0);
        plLeft2.setVelocityY(0);
    } else {
        if (plLeft2.y < gheight / 2) {
            plLeft2.setVelocityY(0);
            plLeft2.y = gheight / 2;
        }
        if (player.y > gheight / 2) {
            player.y = gheight / 2;
            player.setVelocityY(0);
        }
        if (player.x > gwidth * 3 / 4) {
            player.x = gwidth * 3 / 4;
            player.setVelocityX(0);
        }
        if (plLeft2.x > gwidth * 3 / 4) {
            plLeft2.x = gwidth * 3 / 4;
            plLeft2.setVelocityX(0);
        }
    }

    goalKeeperRight.setVelocityX(0);
    goalKeeperLeft.setVelocityX(0);
    this.physics.moveTo(plRight1, ball.x, ball.y, 150);
    this.physics.moveTo(plRight2, ball.x, ball.y, 150);

    if (plRight1.x < gwidth / 4) {
        //plRight1.setVelocityX(velocity*0.5);
        plRight1.x = gwidth / 4;
    }
    if (plRight1.y > gheight / 2) {
        //plRight1.setVelocityY(-velocity*0.5);
        plRight1.y = gheight / 2;
    }
    if (plRight1.x > gwidth - 50) {
        //plRight1.setVelocityX(-1*velocity*0.5);
        plRight1.x = gwidth - 50;
    }
    if (plRight2.x < gwidth / 4) {
        //plRight2.setVelocityX(velocity*0.5);
        plRight2.x = gwidth / 4;
    }
    if (plRight2.y < gheight / 2) {
        //plRight2.setVelocityY(velocity*0.5);
        plRight2.y = gheight / 2;
    }
    if (plRight2.x > gwidth - 50) {
        //plRight2.setVelocityX(-1*velocity*0.5);
        plRight2.x = gwidth - 50;
    }

    if (goalKeeperRight.y > 480) {
        goalKeeperRight.setVelocityY(-velocity * 0.4);
    } else if (goalKeeperRight.y < 320) {
        goalKeeperRight.setVelocityY(velocity * 0.4);
    }
    if (goalKeeperLeft.y > 480) {
        goalKeeperLeft.setVelocityY(-velocity * 0.4);
    } else if (goalKeeperLeft.y < 320) {
        goalKeeperLeft.setVelocityY(velocity * 0.4);
    }


    if (cursorKeys.up.isDown) {
        flag = false;
        player.setVelocityY(-velocity);
        if (plLeft2.y < gheight / 2) {
            plLeft2.setVelocityY(0);
        } else {
            plLeft2.setVelocityY(-velocity);
        }
    } else if (cursorKeys.down.isDown) {
        flag = false;
        if (player.y > gheight / 2) {
            player.setVelocityY(0);
        } else {
            player.setVelocityY(velocity);
        }
        plLeft2.setVelocityY(velocity);
    } else if (!flag) {
        player.setVelocityY(0);
        plLeft2.setVelocityY(0);
    }

    if (cursorKeys.right.isDown) {
        flag = false;
        if (player.x > gwidth * 3 / 4) {
            player.setVelocityX(0);
        } else {
            player.setVelocityX(velocity);
        }
        if (plLeft2.x > gwidth * 3 / 4) {
            plLeft2.setVelocityX(0);
        } else {
            plLeft2.setVelocityX(velocity);
        }
    } else if (cursorKeys.left.isDown) {
        flag = false;
        player.setVelocityX(-velocity);
        plLeft2.setVelocityX(-velocity);
    } else if (!flag) {
        plLeft2.setVelocityX(0);
        player.setVelocityX(0);
    }

    if (endgame) {
        //finalText.setText(' Gooal! ');
        //Phaser.physics.pause();
        player.setVelocity(0, 0);
        plLeft2.setVelocity(0, 0);
        plRight1.setVelocity(0, 0);
        plRight2.setVelocity(0, 0);
        ball.setVelocity(0, 0);
    }
    scoreText.setText(score1 + ' : ' + score0);
}
function hittheball11() {
    ball.setVelocityX((velocity < 0) ? 1.2 * velocity : 1.2 * velocity);
    player.setVelocity(0);
}
function hittheball12() {
    ball.setVelocityX((velocity < 0) ? 1.2 * velocity : 1.2 * velocity);
    plLeft2.setVelocity(0);
}
function hittheball10() {
    ball.setVelocityX((velocity < 0) ? 1.2 * velocity : 1.2 * velocity);
    //plLeft2.setVelocity(0);
}
function hittheball21() {
    ball.setVelocityX((velocity < 0) ? -1.2 * velocity : -1.2 * velocity);
    /*  plRight1.setVelocityX(-1.1*velocity);
     plRight2.setVelocityX(-1.1*velocity); */
}
function hittheball22() {
    ball.setVelocityX((velocity < 0) ? -1.2 * velocity : -1.2 * velocity);
    /*   plRight1.setVelocityX(-1.1*velocity);
      plRight2.setVelocityX(-1.1*velocity); */
}
function hittheball20() {
    ball.setVelocityX((velocity < 0) ? -1.2 * velocity : -1.2 * velocity);
    /*   plRight1.setVelocityX(-1.1*velocity);
      plRight2.setVelocityX(-1.1*velocity); */
}
function goalLeft() {
    gatesL.setVelocityX(0);
    gatesL.setVelocityY(0);
    score0 = score0 + 1;
    stargame();
}
function goalRight() {
    gatesR.setVelocityX(0);
    gatesR.setVelocityY(0);
    score1 = score1 + 1;
    stargame();
}
function stargame() {
    ball.x = gwidth / 2, ball.y = gheight / 2;
    player.x = gwidth / 3, player.y = gheight / 3;
    plLeft2.x = gwidth / 3, plLeft2.y = gheight * 2 / 3;
    goalKeeperLeft.x = 32, goalKeeperLeft.y = 330;
    plRight1.x = gwidth * 2 / 3, plRight1.y = gheight / 3;
    plRight2.x = gwidth * 2 / 3, plRight2.y = gheight * 2 / 3;
    goalKeeperRight.x = 1150, goalKeeperRight.y = 330;
    if (!endgame) {
        ball.setVelocityX(Phaser.Math.Between(-300, 300));
        ball.setVelocityY(Phaser.Math.Between(-300, 300));
    } else {
        ball.setVelocity(0, 0);
    }
    if (score0 == 10) {
        finalText.setText(' Game over. You lose the Game. ');
        endgame = true;
    } else if (score1 == 10) {
        finalText.setText(' Congratulations! You won the Game! ');
        endgame = true;
    } else {
        finalText.setText('');
    }
}
function collideMan1() {
    // //this.physics.moveTo(plRight2, plLeft2.x+50, plLeft2.y+50, 1500);
    // plRight1.setVelocityX(velocity*((player.x > plRight1.x)? -1: 1));
    // player.setVelocityX(velocity*((player.x > plRight1.x)? -1: 1));


}
function collideMan2() {
    //this.physics.moveTo(plRight2, plLeft2.x+50, plLeft2.y+50, 1500);
    // plRight2.setVelocityX(velocity*((plLeft2.x > plRight2.x)? -1: 1));
    // plLeft2.setVelocityX(velocity*((plLeft2.x > plRight2.x)? -1: 1));


}