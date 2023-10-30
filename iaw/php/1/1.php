<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ejercicio 1 php</title>
</head>
<body>
    <?php
        $lanzar = rand(1,2);
        if ($lanzar == 1) {
            print "<img src=./img/cara.jpg>";
        } else if ($lanzar == 2) {
            print "<img src=./img/cruz.jpg>";
        }
    ?>
</body>
</html>