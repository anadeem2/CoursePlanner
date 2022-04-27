<?php
session_start();
$id = 0;
$update = false;
$task = '';
$description = '';
$status = '';

//Connect to mySQL databse
$mysqli = new mysqli('localhost', 'root', '', 'crud') or die(mysqli_error($mysqli));

// INSERT into mySQL database
if (isset($_POST['save'])) {
    $task = $_POST['task'];
    $description = $_POST['description'];
    $status = $_POST['status'];
    
    $mysqli->query("INSERT INTO data (task, description, status) VALUES('$task', '$description', '$status')") or die($mysqli->error);

    $_SESSION['message'] = "Record has been created!";
    $_SESSION['msg_type'] = "success";

    header("Location: index.php");
}


// DELETE from mySQL database
if (isset($_GET['delete'])) {
    $id = $_GET['delete'];
    $mysqli->query("DELETE FROM data WHERE id=$id") or die ($mysqli->error());

    $_SESSION['message'] = "Record has been Deleted!";
    $_SESSION['msg_type'] = "danger";

    header("Location: index.php");
}


//EDIT
if (isset($_GET['edit'])) {
    $id = $_GET['edit'];
    $update = true;
    $result = $mysqli->query("SELECT * FROM data WHERE id=$id") or die($mysqli->error());
    if ($result->num_rows) {
        $row = $result->fetch_array();        
        $task = $row['task'];
        $description = $row['description'];      
        $status = $row['status']; 
    }    
}

if (isset($_POST['update'])){
    $id = $_POST['id'];
    $task = $_POST['task'];
    $description = $_POST['description'];
    $status = $_POST['status'];
    
    $mysqli->query("UPDATE data SET task='$task', description='$description', status='$status' WHERE id=$id") or die($mysqli->error);
    $_SESSION['message'] = "Record has been updated!";
    $_SESSION['msg_type'] = "warning";
    
    header('Location: index.php');
}

?>