<?php
// 连接到数据库
$database = new SQLite3('../../data/password_manager.db');

// 执行查询语句
$query = $database->query('SELECT * FROM Cindy');

// 以关联数组的形式获取查询结果
$results = [];
while ($row = $query->fetchArray(SQLITE3_ASSOC)) {
    $results[] = $row;
}

// 将查询结果转换为 JSON 格式并返回
echo json_encode($results);
?>