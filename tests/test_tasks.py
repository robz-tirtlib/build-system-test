from tasks import Tasks, Task


def test_all_tasks_created(tasks: Tasks):
    for _id in range(1, 9):
        assert Task(str(_id)) in tasks


def test_tasks_dependencies(tasks: Tasks):
    assert tasks.get_task('1').dependencies == []
    assert tasks.get_task('2').dependencies == [Task('1')]
    assert tasks.get_task('3').dependencies == [Task('1')]
    assert tasks.get_task('4').dependencies == [Task('2')]
    assert tasks.get_task('5').dependencies == []
    assert tasks.get_task('6').dependencies == []

    for task in Task('5'), Task('6'):
        assert task in tasks.get_task('7').dependencies

    for task in Task('4'), Task('7'):
        assert task in tasks.get_task('8').dependencies


def test_tasks_sorting(tasks: Tasks):
    assert tasks.get_task('1').id < tasks.get_task('2').id
    assert tasks.get_task('1').id < tasks.get_task('3').id
    assert tasks.get_task('3').id < tasks.get_task('4').id
    assert tasks.get_task('4').id < tasks.get_task('8').id
    assert tasks.get_task('5').id < tasks.get_task('7').id
    assert tasks.get_task('6').id < tasks.get_task('7').id
    assert tasks.get_task('7').id < tasks.get_task('8').id
