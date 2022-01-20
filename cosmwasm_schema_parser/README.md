Hello, my job is to make easier the writing of each class for the contracts.
I read the schemas and translate it into python code.

How to use ?
- Go to project root
- in function `main` line 167, change the name of the contract that you want to parse
- run, you should get a result like:

```py
def instantiate_msg(proposal_deposit, quorum, snapshot_period: int, threshold, timelock_period: int, voting_period: int) -> str:
        return {'proposal_deposit': proposal_deposit, 'quorum': quorum, 'snapshot_period': snapshot_period, 'threshold': threshold, 'timelock_period': timelock_period, 'voting_period': voting_period}

def execute_receive_msg() -> str:
        return {'receive': {}}

def execute_execute_poll_msgs_msg(poll_id: int) -> str:
        return {'execute_poll_msgs': {'poll_id': poll_id}}
```

Now, create a class and copy & paste result