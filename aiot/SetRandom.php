<?php

//0. Get parameters
//1. Connect db
$mysqli = new mysqli("localhost","test123","test123","aiotdb");

// Check connection
if ($mysqli -> connect_errno) {
  echo "Failed to connect to MySQL: " . $mysqli -> connect_error;
  exit();
} 
else
{
     echo "success";
}

//2. query DB
$sqlquary = "update sensors set status=RAND()";
$result = $mysqli -> query($sqlquary);
  

//3. close DB connection
$mysqli -> close();

header("Location: http://localhost/aiot/");
?>