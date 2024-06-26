from typing import Optional
from ..helpers import uihelper as dc

from ...data.dataset_loader import DatasetNN


class TrainWidget(dc.QWidget):

    def __init__(self):
        super().__init__()

        self.btn_start_train = dc.Button(
            "Train", icon=dc.IconM("ma-flash-on-black", color=(255, 255, 0, 255))
        )

        self.sp_lr = dc.DoubleSpinBox(value=0.1, single_step=0.001, decimals=6)
        self.sp_lr.setMinimum(1e-6)
        self.sp_lr.setMaximum(1e3)
        self.sp_lr.setValue(1e-2)
        self.cb_optim = dc.ComboBox(
            selected_item="SGD",
            items=[
                "SGD",
                "SGD with Momentum",
                "ADAM",
            ],
            on_index_changed=self.on_optim_changed,
        )

        self.sp_epochs = dc.SpinBox(range=(1, 1000000), single_step=10, value=100)

        self.cb_batch_mode = dc.ComboBox(
            selected_item="Mini Batch",
            items=["Mini Batch", "Single Batch (all samples)"],
            on_index_changed=self.batch_mode_changed,
        )
        self.sp_batch_size = dc.SpinBox(range=(1, 100), value=100, single_step=1)
        self.max_batch_size = 100

        self.lb_momentum = dc.Label("Momentum:")
        self.sp_momentum = dc.DoubleSpinBox(
            range=(0.001, 1.0), value=0.9, single_step=0.01, decimals=3
        )

        self.lb_beta1 = dc.Label("Beta 1:")
        self.sp_beta1 = dc.DoubleSpinBox(
            range=(0.001, 1.0), value=0.9, single_step=0.001, decimals=3
        )

        self.lb_beta2 = dc.Label("Beta 2:")
        self.sp_beta2 = dc.DoubleSpinBox(
            range=(0.001, 1.0), value=0.999, single_step=0.001, decimals=3
        )

        self.lb_epsilon = dc.Label("Epsilon:")
        self.sp_epsilon = dc.DoubleSpinBox(
            range=(0.00000001, 1.0), value=0.0000001, single_step=0.0000001, decimals=8
        )

        self.ck_store_gradients = dc.CheckBox("Store Gradients")
        self.btn_next_gradient = dc.Button(
            "grad", icon=dc.IconM("ma-navigate-next-black", color=(0, 255, 0, 255))
        )
        self.btn_play_gradient = dc.Button(
            "play", icon=dc.IconM("ma-play-circle-black", color=(0, 255, 0, 255))
        )
        self.btn_prev_gradient = dc.Button(
            "grad", icon=dc.IconM("ma-navigate-before-black", color=(0, 255, 0, 255))
        )
        self.txt_epoch_grad = dc.Label("")
        self.txt_epoch_grad.setMaximumHeight(30)

        dc.Widget(
            widget=self,
            window_ops=dc.WindowOps(title="Train", size=(200, 200)),
            layout=dc.Rows(
                self.btn_start_train,
                dc.NextRow,
                dc.Label("Learning Rate:"),
                dc.NextRow,
                self.sp_lr,
                dc.NextRow,
                dc.Label("Epochs:"),
                dc.NextRow,
                self.sp_epochs,
                dc.NextRow,
                dc.Label("Batch Mode:"),
                dc.NextRow,
                self.cb_batch_mode,
                dc.NextRow,
                dc.Label("Batch Size:"),
                dc.NextRow,
                self.sp_batch_size,
                dc.NextRow,
                dc.Label("Optimizer:"),
                dc.NextRow,
                self.cb_optim,
                dc.NextRow,
                self.lb_momentum,
                dc.NextRow,
                self.sp_momentum,
                dc.NextRow,
                self.lb_beta1,
                dc.NextRow,
                self.sp_beta1,
                dc.NextRow,
                self.lb_beta2,
                dc.NextRow,
                self.sp_beta2,
                dc.NextRow,
                self.lb_epsilon,
                dc.NextRow,
                self.sp_epsilon,
                dc.NextRow,
                self.ck_store_gradients,
                dc.NextRow,
                # dc.Rows(
                self.btn_prev_gradient,
                self.btn_play_gradient,
                self.btn_next_gradient,
                # ),
                dc.NextRow,
                self.txt_epoch_grad,
                dc.VSpacer(),
                align=dc.Align.Top,
            ),
        )

        self.on_optim_changed()

    def on_dataset_changed(self, dataset: DatasetNN) -> None:
        self.max_batch_size = len(dataset)
        self.sp_batch_size.setMaximum(self.max_batch_size)
        self.sp_batch_size.setValue(self.max_batch_size)

    def batch_mode_changed(self, arg1=None) -> None:
        if self.cb_batch_mode.currentText() == "Mini Batch":
            self.sp_batch_size.setEnabled(True)
        else:
            self.sp_batch_size.setValue(self.max_batch_size)
            self.sp_batch_size.setEnabled(False)

    def on_optim_changed(self, arg1=None) -> None:
        optim = self.cb_optim.currentText()
        if optim == "SGD":
            for item in [
                self.lb_momentum,
                self.sp_momentum,
                self.lb_beta1,
                self.sp_beta1,
                self.lb_beta2,
                self.sp_beta2,
                self.lb_epsilon,
                self.sp_epsilon,
                self.ck_store_gradients,
                self.btn_prev_gradient,
                self.btn_play_gradient,
                self.btn_next_gradient,
                self.txt_epoch_grad,
            ]:
                item.setVisible(False)
            self.ck_store_gradients.setChecked(False)
        elif optim == "SGD with Momentum":
            for item in [
                self.lb_beta1,
                self.sp_beta1,
                self.lb_beta2,
                self.sp_beta2,
                self.lb_epsilon,
                self.sp_epsilon,
                self.ck_store_gradients,
                self.btn_prev_gradient,
                self.btn_play_gradient,
                self.btn_next_gradient,
                self.txt_epoch_grad,
            ]:
                item.setVisible(False)
            self.ck_store_gradients.setChecked(False)
            self.lb_momentum.setVisible(True)
            self.sp_momentum.setVisible(True)
        else:
            self.lb_momentum.setVisible(False)
            self.sp_momentum.setVisible(False)
            for item in [
                self.lb_beta1,
                self.sp_beta1,
                self.lb_beta2,
                self.sp_beta2,
                self.lb_epsilon,
                self.sp_epsilon,
                self.ck_store_gradients,
                self.btn_prev_gradient,
                self.btn_play_gradient,
                self.btn_next_gradient,
                self.txt_epoch_grad,
            ]:
                item.setVisible(True)

    def get_parameters(self) -> None:
        out = dict(
            learning_rate=self.sp_lr.value(),
            optim=self.cb_optim.currentText(),
            epochs=self.sp_epochs.value(),
            batch_mode=self.cb_batch_mode.currentText(),
        )

        if out["batch_mode"] == "Mini Batch":
            out["batch_size"] = self.sp_batch_size.value()

        if out["optim"] == "SGD with Momentum":
            out["momentum"] = self.sp_momentum.value()
        elif out["optim"] == "ADAM":
            out["beta1"] = self.sp_beta1.value()
            out["beta2"] = self.sp_beta2.value()
            out["epsilon"] = self.sp_epsilon.value()

        return out
