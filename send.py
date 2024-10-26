import tkinter
from tkinter import ttk
from tkinter import messagebox
import wisepaasdatahubedgesdk.Common.Constants as constant
from wisepaasdatahubedgesdk.EdgeAgent import EdgeAgent
from wisepaasdatahubedgesdk.Model.Edge import EdgeAgentOptions, MQTTOptions, DCCSOptions, EdgeConfig, NodeConfig, DeviceConfig, TextTagConfig


class App():
    def __init__(self, master=None):
        self._edgeAgent = None
        self.master = master
        master.title('SDK Test')
        master.geometry('580x300')

        # Create a tab control
        tabControl = ttk.Notebook(master)

        # Create a tab for DCCS
        dccsTab = ttk.Frame(tabControl, width=200, height=100)
        tabControl.add(dccsTab, text='DCCS')
        tabControl.grid(column=0, row=0, rowspan=2, columnspan=2, padx=8, pady=4, sticky='EWNS')

        # Add tab content for DCCS
        ttk.Label(dccsTab, text='API Url:').grid(column=0, row=0, sticky='EWNS')
        App.apiUrl = tkinter.StringVar()
        App.apiUrl.set('https://api-dccs-ensaas.education.wise-paas.com/')
        tkinter.Entry(dccsTab, textvariable=App.apiUrl, width=40).grid(column=1, row=0, sticky='EWNS')

        ttk.Label(dccsTab, text='Credential Key:').grid(column=0, row=1, sticky='EWNS')
        App.credentialKey = tkinter.StringVar()
        App.credentialKey.set('5b3e3f189df7464e4594d77b02174far')
        tkinter.Entry(dccsTab, textvariable=App.credentialKey, width=40).grid(column=1, row=1, sticky='EWNS')

        # Input fields for velocity, distance, and vehicle count
        ttk.Label(dccsTab, text='Vận tốc:').grid(column=0, row=3, sticky='EWNS')
        App.velocity = tkinter.StringVar()
        tkinter.Entry(dccsTab, textvariable=App.velocity, width=40).grid(column=1, row=3, sticky='EWNS')

        ttk.Label(dccsTab, text='Quãng đường:').grid(column=0, row=4, sticky='EWNS')
        App.distance = tkinter.StringVar()
        tkinter.Entry(dccsTab, textvariable=App.distance, width=40).grid(column=1, row=4, sticky='EWNS')

        ttk.Label(dccsTab, text='Số lượng xe:').grid(column=0, row=5, sticky='EWNS')
        App.vehicle_count = tkinter.StringVar()
        tkinter.Entry(dccsTab, textvariable=App.vehicle_count, width=40).grid(column=1, row=5, sticky='EWNS')

        # Create a tab for MQTT
        mqttTab = ttk.Frame(tabControl, width=200, height=100)
        tabControl.add(mqttTab, text='MQTT')
        tabControl.grid(column=0, row=0, rowspan=2, columnspan=2, padx=8, pady=4)

        # Add tab content for MQTT
        ttk.Label(mqttTab, text='HostName:').grid(column=0, row=0, sticky='EWNS')
        App.hostName = tkinter.StringVar()
        App.hostName.set('127.0.0.1')
        tkinter.Entry(mqttTab, textvariable=App.hostName, width=10).grid(column=1, row=0, sticky='EWNS')

        ttk.Label(mqttTab, text='Port:').grid(column=0, row=1, sticky='EWNS')
        App.port = tkinter.IntVar()
        App.port.set(1883)
        tkinter.Entry(mqttTab, textvariable=App.port, width=10).grid(column=1, row=1, sticky='EWNS')

        ttk.Label(mqttTab, text='Username:').grid(column=0, row=2, sticky='EWNS')
        App.userName = tkinter.StringVar()
        App.userName.set('admin')
        tkinter.Entry(mqttTab, textvariable=App.userName, width=10).grid(column=1, row=2, sticky='EWNS')

        ttk.Label(mqttTab, text='Password:').grid(column=0, row=3, sticky='EWNS')
        App.password = tkinter.StringVar()
        App.password.set('admin')
        tkinter.Entry(mqttTab, textvariable=App.password, width=10).grid(column=1, row=3, sticky='EWNS')

        # Add field for NodeId
        ttk.Label(dccsTab, text='NodeId:').grid(column=0, row=2, sticky='EWNS')
        App.nodeId = tkinter.StringVar()
        App.nodeId.set('413d50f7-6c99-4d81-b11d-79281f270413')
        tkinter.Entry(dccsTab, textvariable=App.nodeId, width=40).grid(column=1, row=2, sticky='EWNS')

        # Connect status
        App.status = tkinter.StringVar()
        App.status.set('Disconnected')
        statusLabel = tkinter.Label(master, textvariable=App.status, bg='#C0C0C0')
        statusLabel.grid(column=2, row=0, columnspan=2, sticky='EWNS')

        # Function for connecting
        def clickedConnect():
            try:
                if App.nodeId.get() == '':
                    messagebox.showwarning("Warning", 'nodeId is necessary')
                    return
                selectTab = tabControl.tab(tabControl.select(), 'text')
                edgeAgentOptions = EdgeAgentOptions(nodeId=App.nodeId.get())
                if selectTab == 'MQTT':
                    edgeAgentOptions.connectType = constant.ConnectType['MQTT']
                    mqttOptions = MQTTOptions(hostName=App.hostName.get(), port=App.port.get(), userName=App.userName.get(), password=App.password.get())
                    edgeAgentOptions.MQTT = mqttOptions
                elif selectTab == 'DCCS':
                    edgeAgentOptions.connectType = constant.ConnectType['DCCS']
                    dccsOptions = DCCSOptions(apiUrl=App.apiUrl.get(), credentialKey=App.credentialKey.get())
                    edgeAgentOptions.DCCS = dccsOptions

                if self._edgeAgent is None:
                    self._edgeAgent = EdgeAgent(edgeAgentOptions)
                    self._edgeAgent.on_connected = on_connected
                    self._edgeAgent.on_disconnected = on_disconnected
                    self._edgeAgent.on_message = on_message
                self._edgeAgent.connect()
            except ValueError as error:
                messagebox.showwarning("Warning", str(error))

        def on_connected(edgeAgent, isConnected):
            if isConnected:
                App.status.set('Connected')
                statusLabel.config(bg='#008000')

        def on_disconnected(edgeAgent, isDisconnected):
            if isDisconnected:
                App.status.set('Disconnected')
                statusLabel.config(bg='#C0C0C0')
                self._edgeAgent = None

        def on_message(edgeAgent, message):
            if message.type == constant.MessageType['ConfigAck']:
                response = 'Upload Config Result: {0}'.format(str(message.message.result))
                messagebox.showinfo("Information", response)

        def clickedDisconnected():
            if self._edgeAgent is None or not self._edgeAgent.isConnected:
                return
            self._edgeAgent.disconnect()

        def clickedSendData():
            if self._edgeAgent is None or not self._edgeAgent.isConnected:
                messagebox.showwarning("Warning", 'edge not connected')
                return
            data = __generateData()
            if data is not None:
                print("Data to send:", data)  # Add this line for debugging
                self._edgeAgent.sendData(data)

        def __generateData():
            config = EdgeConfig()
            nodeConfig = NodeConfig(nodeType=constant.EdgeType['Gateway'])
            config.node = nodeConfig

            deviceConfig = DeviceConfig(
                id='Device2',
                name='Device2',
                description='Device2',
                deviceType='Smart Device',
                retentionPolicyName=''
            )

            # Generate tags based on user input
            vehicleCount = int(App.vehicle_count.get()) if App.vehicle_count.get().isdigit() else 0
            velocity = float(App.velocity.get()) if App.velocity.get().replace('.', '', 1).isdigit() else 0.0
            distance = float(App.distance.get()) if App.distance.get().replace('.', '', 1).isdigit() else 0.0

            textTagVehicleCount = TextTagConfig(
                name='vehicle_count',
                description='Count of vehicles',
                readOnly=False,
                arraySize=0,  # Duy trì giá trị mặc định hoặc đặt đúng theo yêu cầu
            )

            # Nếu `TextTagConfig` yêu cầu một cách khác để thiết lập giá trị,
            # hãy thực hiện thay đổi ở đây.
            # Ví dụ: Nếu cần phải thiết lập giá trị qua một phương thức khác, bạn có thể thêm logic ở đây.

            textTagVelocity = TextTagConfig(
                name='velocity',
                description='Vehicle velocity',
                readOnly=False,
                arraySize=0,
            )

            textTagDistance = TextTagConfig(
                name='distance',
                description='Travel distance',
                readOnly=False,
                arraySize=0,
            )

            # Thêm các thẻ vào deviceConfig
            deviceConfig.textTagList.append(textTagVehicleCount)
            deviceConfig.textTagList.append(textTagVelocity)
            deviceConfig.textTagList.append(textTagDistance)


            config.device = deviceConfig
            return config

        # Create buttons for connecting/disconnecting and sending data
        ttk.Button(master, text='Kết nối', command=clickedConnect).grid(column=0, row=1, sticky='EWNS')
        ttk.Button(master, text='Ngắt kết nối', command=clickedDisconnected).grid(column=1, row=1, sticky='EWNS')
        ttk.Button(master, text='Gửi dữ liệu', command=clickedSendData).grid(column=0, row=2, columnspan=2, sticky='EWNS')

if __name__ == '__main__':
    root = tkinter.Tk()
    app = App(root)
    root.mainloop()
