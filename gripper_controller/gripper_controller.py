import rclpy
from rclpy.node import Node
from ur_msgs.srv import SetIO
from std_msgs.msg import Int32
import time

class GripperController(Node):

    def __init__(self):
        super().__init__('gripper_controller')
        self.cli = self.create_client(SetIO, '/io_and_status_controller/set_io')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Aguardando o serviço /io_and_status_controller/set_io ...')
        
        # Subscription para o comando de abrir/fechar
        self.subscription = self.create_subscription(
            Int32,
            '/gripper_command',
            self.command_callback,
            10)
        self.get_logger().info('GripperController iniciado, aguardando comandos...')

    def enviar_comando_io(self, fun, pin, state):
        """Envia comando de I/O para o serviço UR."""
        req = SetIO.Request()
        req.fun = fun
        req.pin = pin
        req.state = float(state)
        
        future = self.cli.call_async(req)
        future.add_done_callback(self.callback_result)

    def callback_result(self, future):
        try:
            response = future.result()
            self.get_logger().info(f'Resposta do serviço: {response}')
        except Exception as e:
            self.get_logger().error(f'Erro ao chamar o serviço: {e}')

    def fechar_garra(self):
        """Envia o comando para fechar a garra."""
        self.get_logger().info('Fechando garra...')
        self.enviar_comando_io(1, 17, 1)  # Fechar garra
        time.sleep(0.1)  # Delay pequeno para garantir execução
        self.enviar_comando_io(1, 16, 0)  # Garantir que o pino de abrir está em "false"

    def abrir_garra(self):
        """Envia o comando para abrir a garra."""
        self.get_logger().info('Abrindo garra...')
        self.enviar_comando_io(1, 17, 0)  # Garantir que o pino de fechar está em "false"
        time.sleep(0.1)  # Delay pequeno para garantir execução
        self.enviar_comando_io(1, 16, 1)  # Abrir garra

    def command_callback(self, msg):
        """Callback para processar os comandos recebidos do tópico."""
        command = msg.data
        self.get_logger().info(f'Comando recebido: {command}')
        if command == 1:
            self.fechar_garra()
        elif command == 0:
            self.abrir_garra()
        else:
            self.get_logger().warn(f'Comando inválido recebido: {command}')


def main(args=None):
    rclpy.init(args=args)
    gripper_controller = GripperController()
    rclpy.spin(gripper_controller)
    gripper_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
