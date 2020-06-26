import {NgModule, NO_ERRORS_SCHEMA} from "@angular/core";
import {HomeComponent} from "~/app/plantlet/home/home.component";
import {NativeScriptRouterModule} from "nativescript-angular";
import {NativeScriptCommonModule} from "nativescript-angular/common";
import {SharedModule} from "~/app/shared/shared.module";
import {DropDownModule} from "nativescript-drop-down/angular";


@NgModule({
    declarations: [HomeComponent],
    imports: [
        NativeScriptRouterModule,
        NativeScriptCommonModule,
        NativeScriptRouterModule.forChild([
            {path: '', component: HomeComponent}
        ]),
        SharedModule,
        DropDownModule
    ],
    schemas: [NO_ERRORS_SCHEMA]
})
export class HomeModule {

}
