import os
import csv

MAX_RECORDS = 10


class Records:
    filename = "records.csv"
    file_dir = os.path.dirname(os.path.realpath(__file__))

    def __init__(self):
        self.game_records = []
        self.data_path = os.path.join(os.path.dirname(self.file_dir), 'data')
        self.file_path = os.path.join(self.data_path, self.filename)
        self.check_records()

    def check_records(self):
        if not os.path.isdir(self.file_path):
            os.makedirs(self.file_path)
            print(' No habia directoria para guardar los registros')
        if not os.path.exists(self.file_path):
            self.reset_records()

    def insert_record(self, nombre, puntuacion):
        pass

    def es_puntuacion_menor(self):
        pass

    def save_records(self):

        with open(self.file_path, 'w') as records_file:
            writer = csv.writer(records_file)
            writer.writerow(('Nombre', 'Puntuación'))
            writer.writerows(self.game_records)
            records_file.close()

    def load_records(self):
        pass

    def reset_records(self):

        self.game_records = []
        for cont in range(MAX_RECORDS):
            self.game_records.append(['-----', 0])
        self.save_records()
