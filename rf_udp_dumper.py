#!/usr/bin/env python3

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys

    UDP_ADDR = input("Input UDP address (localhost for localhost): ")
    if UDP_ADDR.lower() == "localhost":
        UDP_ADDR = "127.0.0.1"

    while True:
        try:
            UDP_PORT = int(input("Input UDP port: "))
            if UDP_PORT >= 1 and UDP_PORT <= 65535:
                dev_args = input("Input device arguments: ")
                break

            else:
                raise ValueError

        except ValueError:
            print(f"\nValue: {UDP_PORT} in not valid. Please input an integer number between 1 and 65535\n")
            continue

    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import network
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import osmosdr
import time

from gnuradio import qtgui

print(f"\nRunning UDP server on {UDP_ADDR}:{UDP_PORT}\n")

class untitled(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, f"RF Spectrum [UDP]({UDP_ADDR}:{UDP_PORT})", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle(f"RF Spectrum [UDP]({UDP_ADDR}:{UDP_PORT}) <{dev_args}>")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "untitled")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        self.RF_gain = RF_gain = 30
        self.IF_gain = IF_gain = 30
        self.FREQ = FREQ = 10e6
        self.BB_gain = BB_gain = 30
        self.samp_rate = samp_rate = 48000
        self.min_freq = min_freq = 1
        self.max_freq = max_freq = 2e9
        self.RF_gain_value = RF_gain_value = RF_gain
        self.IF_gain_value = IF_gain_value = IF_gain
        self.FREQ_value = FREQ_value = FREQ
        self.BB_gain_value = BB_gain_value = BB_gain

        self._RF_gain_range = Range(1, 100, 1, 30, 1)
        self._RF_gain_win = RangeWidget(self._RF_gain_range, self.set_RF_gain, "RF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._RF_gain_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._IF_gain_range = Range(1, 100, 1, 30, 1)
        self._IF_gain_win = RangeWidget(self._IF_gain_range, self.set_IF_gain, "IF Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._IF_gain_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._FREQ_range = Range(min_freq, max_freq, 1, 10e6, 1)
        self._FREQ_win = RangeWidget(self._FREQ_range, self.set_FREQ, "Frequency", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._FREQ_win, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._BB_gain_range = Range(1, 100, 1, 30, 1)
        self._BB_gain_win = RangeWidget(self._BB_gain_range, self.set_BB_gain, "BB Gain", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._BB_gain_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=1,
                decimation=5,
                taps=[],
                fractional_bw=0)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            32768,
            window.WIN_BLACKMAN_hARRIS,
            0,
            samp_rate,
            "",
            1,
            None
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.001)
        self.qtgui_freq_sink_x_0.set_y_axis(-140, 100)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(True)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(0.1)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(True)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_0_win)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + dev_args
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(FREQ, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(RF_gain, 0)
        self.osmosdr_source_0.set_if_gain(IF_gain, 0)
        self.osmosdr_source_0.set_bb_gain(BB_gain, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_gr_complex, 1, UDP_ADDR, UDP_PORT, 0, 1472, False)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, 1000000,True)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=200000,
        	audio_decim=4,
        	deviation=150000,
        	audio_pass=15000,
        	audio_stop=16000,
        	gain=1.0,
        	tau=75e-6,
        )
        self._RF_gain_value_tool_bar = Qt.QToolBar(self)

        if None:
            self._RF_gain_value_formatter = None
        else:
            self._RF_gain_value_formatter = lambda x: eng_notation.num_to_str(x)

        self._RF_gain_value_tool_bar.addWidget(Qt.QLabel("RF Gain: "))
        self._RF_gain_value_label = Qt.QLabel(str(self._RF_gain_value_formatter(self.RF_gain_value)))
        self._RF_gain_value_tool_bar.addWidget(self._RF_gain_value_label)
        self.top_grid_layout.addWidget(self._RF_gain_value_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._IF_gain_value_tool_bar = Qt.QToolBar(self)

        if None:
            self._IF_gain_value_formatter = None
        else:
            self._IF_gain_value_formatter = lambda x: eng_notation.num_to_str(x)

        self._IF_gain_value_tool_bar.addWidget(Qt.QLabel("IF Gain: "))
        self._IF_gain_value_label = Qt.QLabel(str(self._IF_gain_value_formatter(self.IF_gain_value)))
        self._IF_gain_value_tool_bar.addWidget(self._IF_gain_value_label)
        self.top_grid_layout.addWidget(self._IF_gain_value_tool_bar, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._FREQ_value_tool_bar = Qt.QToolBar(self)

        if None:
            self._FREQ_value_formatter = None
        else:
            self._FREQ_value_formatter = lambda x: eng_notation.num_to_str(x)

        self._FREQ_value_tool_bar.addWidget(Qt.QLabel("Frequency:"))
        self._FREQ_value_label = Qt.QLabel(str(self._FREQ_value_formatter(self.FREQ_value)))
        self._FREQ_value_tool_bar.addWidget(self._FREQ_value_label)
        self.top_grid_layout.addWidget(self._FREQ_value_tool_bar, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._BB_gain_value_tool_bar = Qt.QToolBar(self)

        if None:
            self._BB_gain_value_formatter = None
        else:
            self._BB_gain_value_formatter = lambda x: eng_notation.num_to_str(x)

        self._BB_gain_value_tool_bar.addWidget(Qt.QLabel("BB Gain: "))
        self._BB_gain_value_label = Qt.QLabel(str(self._BB_gain_value_formatter(self.BB_gain_value)))
        self._BB_gain_value_tool_bar.addWidget(self._BB_gain_value_label)
        self.top_grid_layout.addWidget(self._BB_gain_value_tool_bar, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)

        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.network_udp_sink_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_fm_demod_cf_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_throttle_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "untitled")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_RF_gain(self):
        return self.RF_gain

    def set_RF_gain(self, RF_gain):
        self.RF_gain = RF_gain
        self.set_RF_gain_value(self.RF_gain)
        self.osmosdr_source_0.set_gain(self.RF_gain, 0)

    def get_IF_gain(self):
        return self.IF_gain

    def set_IF_gain(self, IF_gain):
        self.IF_gain = IF_gain
        self.set_IF_gain_value(self.IF_gain)
        self.osmosdr_source_0.set_if_gain(self.IF_gain, 0)

    def get_FREQ(self):
        return self.FREQ

    def set_FREQ(self, FREQ):
        self.FREQ = FREQ
        self.set_FREQ_value(self.FREQ)
        self.osmosdr_source_0.set_center_freq(self.FREQ, 0)

    def get_BB_gain(self):
        return self.BB_gain

    def set_BB_gain(self, BB_gain):
        self.BB_gain = BB_gain
        self.set_BB_gain_value(self.BB_gain)
        self.osmosdr_source_0.set_bb_gain(self.BB_gain, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.qtgui_freq_sink_x_0.set_frequency_range(0, self.samp_rate)

    def get_min_freq(self):
        return self.min_freq

    def set_min_freq(self, min_freq):
        self.min_freq = min_freq

    def get_max_freq(self):
        return self.max_freq

    def set_max_freq(self, max_freq):
        self.max_freq = max_freq

    def get_RF_gain_value(self):
        return self.RF_gain_value

    def set_RF_gain_value(self, RF_gain_value):
        self.RF_gain_value = RF_gain_value
        Qt.QMetaObject.invokeMethod(self._RF_gain_value_label, "setText", Qt.Q_ARG("QString", str(self._RF_gain_value_formatter(self.RF_gain_value))))

    def get_IF_gain_value(self):
        return self.IF_gain_value

    def set_IF_gain_value(self, IF_gain_value):
        self.IF_gain_value = IF_gain_value
        Qt.QMetaObject.invokeMethod(self._IF_gain_value_label, "setText", Qt.Q_ARG("QString", str(self._IF_gain_value_formatter(self.IF_gain_value))))

    def get_FREQ_value(self):
        return self.FREQ_value

    def set_FREQ_value(self, FREQ_value):
        self.FREQ_value = FREQ_value
        Qt.QMetaObject.invokeMethod(self._FREQ_value_label, "setText", Qt.Q_ARG("QString", str(self._FREQ_value_formatter(self.FREQ_value))))

    def get_BB_gain_value(self):
        return self.BB_gain_value

    def set_BB_gain_value(self, BB_gain_value):
        self.BB_gain_value = BB_gain_value
        Qt.QMetaObject.invokeMethod(self._BB_gain_value_label, "setText", Qt.Q_ARG("QString", str(self._BB_gain_value_formatter(self.BB_gain_value))))




def main(top_block_cls=untitled, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
