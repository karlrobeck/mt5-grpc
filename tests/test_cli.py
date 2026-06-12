from unittest.mock import MagicMock, patch
from click.testing import CliRunner
import logging
from src.main import cli

def test_cli_verbose_flag():
    runner = CliRunner()
    mock_server = MagicMock()

    with patch('grpc.server', return_value=mock_server) as mock_grpc_server, \
         patch('logging.basicConfig') as mock_basic_config:
         
        # Run command without verbose
        result = runner.invoke(cli, ['serve', '--port', '9090'])
        assert result.exit_code == 0
        mock_basic_config.assert_called_with(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
    with patch('grpc.server', return_value=mock_server) as mock_grpc_server, \
         patch('logging.basicConfig') as mock_basic_config:
         
        # Run command with verbose
        result = runner.invoke(cli, ['serve', '--port', '9090', '--verbose'])
        assert result.exit_code == 0
        mock_basic_config.assert_called_with(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

    with patch('grpc.server', return_value=mock_server) as mock_grpc_server, \
         patch('logging.basicConfig') as mock_basic_config:
         
        # Run command with short option -v
        result = runner.invoke(cli, ['serve', '--port', '9090', '-v'])
        assert result.exit_code == 0
        mock_basic_config.assert_called_with(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
