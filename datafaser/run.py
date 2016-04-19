import datafaser.operations


class Runner:

    def __init__(self, data, operations=None):
        """
        :param data: datafaser.data.Data object
        :param operations: map of operation names to functions implementing them
        """

        self.data = data
        self.operations = operations or datafaser.operations.get_default_operations_map(data)
        self.phase_number = 0

    def load_and_run_all_plans(self):
        """
        Runs plans as long as any are available at `datafaser.run.plan`.
        """

        while len(self.data.dig('datafaser.run.plan')) > 0:
            self.phase_number += 1
            run = self.data.dig('datafaser.run')
            phase = run['plan'].pop()
            if isinstance(phase, dict) and len(phase) == 1:
                run['phase'] = phase
                for phase_name, operations in phase.items():
                    print('Running phase #%d: "%s"' % (self.phase_number, phase_name))
                    self.run_operation(operations)
                run['done'].append(phase)
                del run['phase']
            else:
                raise ValueError(
                        'Phase #%d in plan does not map one name to operations: %s' %
                        (self.phase_number, str(phase))
                )

    def run_operation(self, operations):
        """
        :param operations: list of operations: a map from operation name to its parameter structure.
        """

        for step in operations:
            for operation in step.keys():
                if operation in self.operations:
                    print('Run operation "%s"' % operation)
                    self.operations[operation](self.data, step[operation])
                else:
                    raise ValueError('Unknown operation: "%s"' % operation)