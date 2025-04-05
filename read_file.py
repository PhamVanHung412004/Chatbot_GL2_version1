from package import pd
class Read_File:
    def __init__(self, path : str = None) -> None:
        '''
        path : duong dan cua file csv
        '''
        self.path : str = path

class Read_File_CSV(Read_File):
    def __init__(self, path : str) -> None:
        super().__init__(path)
    def run(self) -> pd.core.frame.DataFrame:
        return pd.read_csv(self.path)