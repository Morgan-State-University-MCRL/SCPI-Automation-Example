﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using Ivi.Visa;
using OxyPlot;
using OxyPlot.Series;


namespace CurveQuery
{
    public partial class frmCurveQuery : Form
    {
        private IMessageBasedSession scope = null;
        private Dictionary<string, OxyColor> channelColors = null;

        public frmCurveQuery()
        {
            InitializeComponent();

            dropDownCH.SelectedIndex = 0;

            channelColors = new Dictionary<string, OxyColor>()
            {
                { "CH1", OxyColor.FromRgb(255, 247, 57) },
                { "CH2", OxyColor.FromRgb(33, 207, 214) },
                { "CH3", OxyColor.FromRgb(231, 69, 99) },
                { "CH4", OxyColor.FromRgb(148, 207, 49) }
            };
        }

        private void btnGetWaveform_Click(object sender, EventArgs e)
        {
            plotView.Model = null;
            Application.DoEvents();

            try
            {
                // Open connection to the instrument
                scope = GlobalResourceManager.Open(txtVisaRsrcAddr.Text) as IMessageBasedSession;

                // Good practice to flush the message buffers and clear the instrument status upon connecting.
                scope.Clear();
                scope.FormattedIO.WriteLine("*CLS");

                // Query the instrument ID and display
                scope.FormattedIO.WriteLine("*IDN?");
                txtInstrumentID.Text = scope.FormattedIO.ReadLine().Trim();
                Application.DoEvents(); // Allows the UI to update before this method returns

                // Setup the data transfer settings
                scope.FormattedIO.WriteLine($"DATA:SOUR {dropDownCH.Text}");
                scope.FormattedIO.WriteLine("DAT:ENC RIB");     // Signed Binary LSB Format
                scope.FormattedIO.WriteLine("DATA:WIDTH 2");    // 2 bytes per point

                // Query horizontal scaling factors
                scope.FormattedIO.WriteLine("WFMO:XINCR?");
                double xinc = Double.Parse(scope.FormattedIO.ReadString());
                scope.FormattedIO.WriteLine("WFMO:XZEro?");
                double xzero = Double.Parse(scope.FormattedIO.ReadString());
                scope.FormattedIO.WriteLine("WFMO:PT_OFF?");
                long pt_off = Int64.Parse(scope.FormattedIO.ReadString());
                scope.FormattedIO.WriteLine("WFMO:XUNit?");
                string xunits = scope.FormattedIO.ReadString().Trim();

                // Query vertical scaling factors
                scope.FormattedIO.WriteLine("WFMO:YMUlt?");
                double ymult = Double.Parse(scope.FormattedIO.ReadString());
                scope.FormattedIO.WriteLine("WFMO:YZEro?");
                double yzero = Double.Parse(scope.FormattedIO.ReadString());
                scope.FormattedIO.WriteLine("WFMO:YOFf?");
                double yoff = Double.Parse(scope.FormattedIO.ReadString());
                scope.FormattedIO.WriteLine("WFMO:YUNit?");
                string yunits = scope.FormattedIO.ReadString();

                // Fetch the raw waveform data
                scope.FormattedIO.WriteLine("CURVE?");
                short[] rawData = scope.FormattedIO.ReadLineBinaryBlockOfInt16();

                // Create an OxyPlot LineSeries to put the data into
                LineSeries waveformData = new LineSeries();
                waveformData.Title = dropDownCH.Text;
                waveformData.StrokeThickness = 2;
                waveformData.LineStyle = LineStyle.Solid;
                waveformData.Color = channelColors[dropDownCH.Text];

                // Convert the raw integer data to floating point values and load into the LineSeries
                double t0 = (-pt_off * xinc) + xzero;
                double xval, yval;
                for (int i = 0; i < rawData.Length; i++)
                {
                    // Formula for creating X values
                    xval = t0 + (xinc * i);

                    // Formula for creating Y values
                    yval = (((double)rawData[i] - yoff) * ymult) + yzero;
                    waveformData.Points.Add(new DataPoint(xval, yval));
                }

                // Create a plot to display the LineSeries on
                var waveformPlot = new PlotModel { Title = "Waveform Plot" };
                waveformPlot.PlotType = PlotType.XY;
                waveformPlot.Series.Add(waveformData);

                // Add a legend to the plot
                var legend = new OxyPlot.Legends.Legend();
                legend.LegendBackground = OxyColor.FromRgb(255, 255, 255);
                legend.LegendBorder = OxyColor.FromRgb(0,0,0);
                legend.LegendBorderThickness = 1;
                waveformPlot.Legends.Add(legend);

                // Add Axis to the plot
                OxyPlot.Axes.LinearAxis xAxis = new OxyPlot.Axes.LinearAxis();
                xAxis.Position = OxyPlot.Axes.AxisPosition.Bottom;
                xAxis.Unit = xunits;
                xAxis.Title = "Time";

                OxyPlot.Axes.LinearAxis yAxis = new OxyPlot.Axes.LinearAxis();
                yAxis.Position = OxyPlot.Axes.AxisPosition.Left;
                yAxis.Unit = yunits;
                yAxis.Title = "Amplitude";

                waveformPlot.Axes.Add(xAxis);
                waveformPlot.Axes.Add(yAxis);

                // Load the plot into the plot view
                plotView.Model = waveformPlot;
            }
            catch(Exception ex)
            {
                MessageBox.Show(ex.Message, "Exception Occurred", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
                if (scope != null)
                {
                    scope.Dispose();
                }
            }
        }
    }
}
