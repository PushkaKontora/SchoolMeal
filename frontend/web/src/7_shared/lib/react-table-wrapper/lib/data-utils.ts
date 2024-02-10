export function updateDataState<DataRow>(
  setter: React.Dispatch<React.SetStateAction<DataRow[]>>,
  rowIndex: number, columnKey: string, value: unknown) {
  setter(prev => 
    prev.map((row, index) => {
      if (index == rowIndex) {
        return {
          ...prev[rowIndex],
          [columnKey]: value
        };
      }
      return row;
    })
  );
}
