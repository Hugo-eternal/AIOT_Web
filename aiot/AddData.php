<?php

//0. Get parameters
$light = 0;
$humi = 0;
$temp = 0;
if (!empty($_GET["light"])) 
{
    $light = $_GET["light"];
}
if (!empty($_GET["humi"])) 
{
    $humi = $_GET["humi"];
}
if (!empty($_GET["temp"])) 
{
    $temp = $_GET["temp"];
}
//1. Connect db
$mysqli = new mysqli("localhost","test123","test123","aiotdb");

// Check connection
if ($mysqli -> connect_errno) {
  echo "Failed to connect to MySQL: " . $mysqli -> connect_error;
  exit();
} 
else
{
    echo "Success";
}

//2. query DB
$sqlquary = "INSERT INTO sensors (light,humi,temp) VALUES ($light,$humi,$temp)";
$result = $mysqli -> query($sqlquary);
  

//3. close DB connection
$mysqli -> close();

header("Location: http://localhost/aiot/");
?>