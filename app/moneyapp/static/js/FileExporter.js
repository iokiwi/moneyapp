const _EXPORT_EMPLEMENT_ERROR = "Export method has not been implemented.";

class FileExporter{
    constructor(data){
        this.data = data;
    }
    export(){
        throw new NotImplementedError(_EXPORT_EMPLEMENT_ERROR);
    }
}

class JSONExporter extends FileExporter{
    export(){
        const jsonData = JSON.stringify(this.data, null, 2);

        const dataUri = "data:application/json;charset=utf-8," + encodeURIComponent(jsonData);

        const downloadLink = document.createElement("a");
        downloadLink.href = dataUri;
        downloadLink.download = "exported_data.json";
        downloadLink.click();
    }
}