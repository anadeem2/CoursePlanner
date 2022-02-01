<!DOCTYPE html>
<html>
<head>


    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css" integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO" crossorigin="anonymous">
    <title>ToDoList</title>
</head>

<body>

    <?php require_once 'process.php' ?>

    <div class="alert alert-<?=$_SESSION['msg_type']?>">
        <?php 
        echo $_SESSION['message'];
        unset($_SESSION['message']);
        ?>
    </div>
    <?php endif ?>

    <div class="container">
       
        <?php
            $mysqli = new mysqli('localhost', 'root', '', 'crud') or die(mysqli_error($mysqli));
            $result = $mysqli->query("SELECT * FROM data") or die($mysqli->error);
        ?>
        <div class="row justify-content-center">
            <table class="table">
                <thead>
                    <tr>
                        <th>Task</th>
                        <th>Description</th>
                        <th>Status</th>
                        <th colspan="2">Action</th>
                    </tr>
                    <?php while ($row = $result->fetch_assoc()): ?>
                    <tr>
                        <td><?php echo $row['task']; ?></td>
                        <td><?php echo $row['description']; ?></td>
                        <td><?php echo $row['status']; ?></td>
                        <td>
                            <a href="index.php?edit=<?php echo $row['id']; ?>" class="btn btn-info">Edit</a>
                            <a href="process.php?delete=<?php echo $row['id']; ?>" class="btn btn-danger">Delete</a>
                        </td>
                    </tr>
                    <?php endwhile; ?>
                </thead>
            </table>
        </div>

        <?php function pre_r($array) { echo '<pre>'; print_r($array); echo '</pre>'; } ?>
        
        <div class="row justify-content-center">
            <form action="process.php" method="POST">
                <input type="hidden" name="id" value="<?php echo $id; ?>">
                <div class="form-group">
                    <label for="">Task</label>
                    <input type="text" name="task" class="form-control" value="<?php echo $task; ?>" placeholder="Enter task">
                </div>
                <div class="form-group">
                    <label for="">Description</label>
                    <input type="text" name="description" class="form-control" value="<?php echo $description; ?>" placeholder="Brief description">
                </div>
                <div class="form-group">
                    <label for="">Status</label>
                    <input type="text" name="status" class="form-control" value="<?php echo $status; ?>" placeholder="Completed/InProgress">
                </div>
                <div class="form-group">
                    <?php if ($update == true): ?>
                    <button type="submit" class="btn btn-warning" name="update">Update</button>
                    <?php else: ?>
                    <button type="submit" class="btn btn-primary" name="save" value="saveCourse">Save</button>
                    <?php endif; ?>
                </div>
            </form>
        </div>
    </div>

    <!-- JavaScript (Opcional) -->
    <!-- jQuery primeiro, depois Popper.js, depois Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js" integrity="sha384-ZMP7rVo3mIykV+2+9J3UJ46jBk0WLaUAdn689aCwoqbBJiSnjAK/l8WvCWPIPm49" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js" integrity="sha384-ChfqqxuZUCnJSK3+MXmPNIyE6ZbWh2IMqE241rYiqJxyMiZ6OW/JmZQ5stwEULTy" crossorigin="anonymous"></script>
    
</body>
</html>